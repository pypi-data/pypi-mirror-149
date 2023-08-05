import json
import os
import re
import shutil
import subprocess
import sys
import hail as hl
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class wdlplayer(object):
    def __init__(self, outdir, filedir, localdata=None, tmpdir=None, config=None, wdl=None, inputs=None):
        
        # Assigns outdir and tmpdir
        self.outdir = outdir
        self.filedir = filedir
        self.localdata = localdata if localdata is not None else self.outdir
        localdata = self.localdata
        self.tmpdir = tmpdir if tmpdir is not None else os.path.join(
            self.outdir, '.caper_tmp')
            
        # Assigns config json path
        self.config = config
        self.wdl = wdl
        self.metadata = None
        self.uid = None
        
        #---------------------------------------------------
        # Same as hailrunner
        # to keep syntax, change outdir
        self.outdir = filedir

        # Define version
        self.version = 'debug' if 'VERSION' not in os.environ else os.environ['VERSION']

        # Create outdir and basic .jobs file structure
        if not os.path.isdir(self.outdir) or not os.path.isdir(os.path.join(self.outdir, 'log', self.version)):
            os.makedirs(os.path.join(self.outdir, "log", self.version) + '/')
        self.logdir = os.path.join(self.outdir, 'log', self.version)

        if not os.path.isdir(os.path.join(self.outdir, 'script', self.version)):
            os.makedirs(os.path.join(
                self.outdir, "script", self.version) + '/')
        self.scriptdir = os.path.join(self.outdir, 'script', self.version)
        
        # add current links
        if os.path.isdir(os.path.join(self.outdir, "current")):
            shutil.rmtree(os.path.join(self.outdir, "current"))
        os.makedirs(os.path.join(self.outdir, "current"))
        os.symlink(self.logdir, os.path.join(
            self.outdir, 'current', 'log'), target_is_directory=True)
        os.symlink(self.scriptdir, os.path.join(
            self.outdir, 'current', 'script'), target_is_directory=True)
        
        # add local /data folder links
        if localdata != '':
            if os.path.islink(os.path.join(self.outdir, 'data')):
                os.remove('data')
            os.symlink(localdata, os.path.join(
                self.outdir, 'data'), target_is_directory=True)
        
        # 0-based counter for submits made in script. Used for naming and tracking.
        self.current_run = 0

        # 0-based counter that stores a particular run count for restoration later
        self._setr = []
        self._sig_popr = None

        # Initialize run-specific array attributes of PyRunner class
        self.current_job = []

        #---------------------------------------------------

        # Read in inputfofn can be a list of files or read from a file
        self.fofn = []
        if isinstance(inputs, str):
            self.fofn.append(inputs)
        else:
            self.fofn.append('')

        #---------------------------------------------------
        # fix outdir
        self.outdir = outdir

        self.get_jars()

    def get_jars(self):
        lines = [line.strip() for line in open(
            os.path.join(os.environ['HOME'], '.caper/default.conf'), 'r')]
        self.cromwell_jar = [line.split('=')[1]
                            for line in lines if re.search('^cromwell', line)][0]
        self.womtool_jar = [line.split('=')[1]
                            for line in lines if re.search('^womtool', line)][0]

    def submit(self, name, wdl, inputs, server=False, gcp=False, port=8000, silent=False):
    
        #---------------------------------------------------
        # hailrunner (modded from submit_job)
        if len(self.fofn) == self.current_run + 1:
            self.fofn.append([])
        self.current_job = [wdl, inputs]
        self.fofn[self.current_run + 1] = self.outdir
    
        #---------------------------------------------------
        # checkpointing
        log_path = os.path.join(
            self.logdir, "run{}.{}.json".format(self.current_run + 1, name))
        
        if os.path.exists(log_path):
            self.metadata = json.load(open(log_path, 'r'))
            if self.metadata['status'] != 'Succeeded':
                self.uid = self.metadata['id']
                self.metadata = self.get_metadata(self.uid)
                if self.metadata['status'] != 'Succeeded':
                    raise Exception(f'Job {self.uid} has not succeeded.')                
            logger.info('Run {} successfully completed in an earlier attempt.'.format(
                self.current_run + 1))
            outfile = os.path.join(self.metadata['workflowRoot'], 'metadata.json')
            self._process_job_outputs(outfile, log_path)
        else:            
            #---------------------------------------------------
            # Specify script and log path
            script_path = os.path.join(
                self.scriptdir,
                "run{}.{}".format(self.current_run + 1, name)
            )
            
            if os.path.isfile(self.current_job[0]):
                shutil.copy2(self.current_job[0], f'{script_path}.wdl')
            if isinstance(inputs, str) and os.path.isfile(self.current_job[1]):
                shutil.copy2(self.current_job[1], f'{script_path}.json')
            
            if isinstance(inputs, dict):
                json.dump(inputs, open(
                    f'{script_path}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                inputs = f'{script_path}.json'
                    
            #---------------------------------------------------
            # command
            cmd = ['caper']
            
            # SERVER or RUN mode
            if server:
                cmd.extend(['submit'])
            else:
                cmd.extend(['run'])

            # specify wdl, inputs and label
            cmd.extend([wdl,
                        '--inputs', inputs,  
                        '--str-label', name
                        ])

            # define options using command or config file
            if self.config is not None:
                # use config to specify RUN or SERVER mode
                cmd.extend(['--conf', self.config])
            elif not server:
                # specify backend options in RUN mode
                # otherwise, need to be specified in PORT mode
                if gcp:
                    cmd.extend([
                        '--backend', 'gcp',
                        '--gcp-prj', self.project,
                        '--gcp-zones', self.zone,
                        '--gcp-out-dir', self.outdir,
                        '--gcp-loc-dir', self.tmpdir,
                        '--use-google-cloud-life-sciences'
                    ])
                else:
                    cmd.extend(['--backend', 'local'])
                    cmd.extend(['--local-out-dir', self.outdir])
                    cmd.extend(['--local-loc-dir', self.tmpdir])
            elif server:
                # specify PORT to connect in SERVER mode
                # other backend options are defined in the server itself
                cmd.extend([
                    '--port', str(port),
                    '--gcp-loc-dir', self.tmpdir
                    ])
            
            #---------------------------------------------------
            # execute
            output = self._execute(cmd, silent)
            if not server:
                outfile = self._parse_run_output(output)
                self._process_job_outputs(outfile, log_path)
            elif server:
                # return uid without "completing" job
                self.uid = self._parse_server_output(output)
                print('Pausing to let backend write metadata...')
                time.sleep(15)
                self.metadata = self.get_metadata(self.uid)
                self.write_json(log_path, self.metadata)
                return(self.metadata)
        
        #---------------------------------------------------
        # done (from hailrunner)
        self.done(outfile)
        
        return(outfile)
    
    def _execute(self, cmd, silent=False):
        logger.info('Command: {}'.format(' '.join(cmd)))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=0)

        output = []
        for line in iter(process.stdout.readline, ''):
            if not silent:
                sys.stdout.write(line)
                sys.stdout.flush()
            output.append(line.strip())

        process.stdout.close()
        return(output)
    
    def _parse_run_output(self, output):
        line = [line for line in output if re.search(
            'Wrote metadata file.', line)][0]
        outfile = re.search('Wrote metadata file. (.*)', line).group(1)
        outdir = '/'.join(outfile.split('/')[0:-2])
        uid = outfile.split('/')[-2]
        return(outfile)

    def _parse_server_output(self, output):
        line = [line for line in output if re.search(
            "'id': \'(.*)\'\,", line)][0]
        uid = re.search("'id': \'(.*)\'\,", line).group(1)
        return(uid)

    def _process_job_outputs(self, outfile, log_path):
        if outfile[0:3] == 'gs:':
            self.metadata = json.load(hl.hadoop_open(outfile, 'r'))
        else:
            self.metadata = json.load(open(outfile, 'r'))
            
        json.dump(self.metadata, open(log_path, 'w', encoding='utf-8'), ensure_ascii = False, indent = 4)
        
        if os.path.exists(f'{self.filedir}/cromwell.out'):
            shutil.move(f'{self.filedir}/cromwell.out',
                os.path.splitext(log_path)[0] + '.out')

    def get_inputs(self, wdl):
        cmd = ["java", "-jar", self.womtool_jar, "inputs", wdl]
        p = subprocess.run(cmd, capture_output=True)
        output, error = p.stdout.decode().strip(), p.stderr.decode().strip()
        inputs = json.loads(output)
        print(inputs)
        return(output)

    def get_outputs(self, metadata=None):
        metadata = self.f if metadata is None else metadata
        jdict = json.load(hl.hadoop_open(metadata, 'r'))
        return(jdict['outputs'])

    def list(self, uid=None):
        'server mode only'
        uid = uid if uid is not None else self.uid
        cmd = ['caper', 'list', uid]
        p = subprocess.run(cmd, capture_output=True)
        output, error = p.stdout.decode().strip(), p.stderr.decode().strip()
        return(output)
    
    def get_metadata(self, uid=None):
        'server mode only'
        uid = uid if uid is not None else self.uid
        cmd = ['caper', 'metadata', uid]
        p = subprocess.run(cmd, capture_output=True)
        output, error = p.stdout.decode().strip(), p.stderr.decode().strip()
        metadata = json.loads(output)
        return(metadata)
    
    def get_status(self, uid=None):
        metadata = self.get_metadata(uid)
        return(metadata['status'])

    def done(self, outfile, abspath=False):
        #----
        if self.metadata['status'] != 'Succeeded':
            raise Exception('Cromwell did not finish successfully.')

        self.fofn[self.current_run + 1] = outfile
        self.current_run += 1
        if self._sig_popr:
            self._sig_popr = False
            self._setr.pop()
        
        #----
        with open(os.path.join(self.logdir, 'output.fofn'), 'w') as f:
            if abspath:
                fofn = [os.path.abspath(filename) for filename in self.fofn]
            else:
                fofn = self.fofn
            f.write('\n'.join(fofn) + '\n')

    def write_json(self, outfile, jdict):
        json.dump(jdict, open(outfile, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=4)

    def test_env(self):
        cmd = ['which', 'pip']
        p = subprocess.run(cmd, capture_output=True)
        _, error = p.stdout.decode().strip(), p.stderr.decode().strip()
        return(error)

    #---------------------------------------------------
    # hailrunner (properties)

    @property
    def r(self):
        return(self.current_run)
    
    @property
    def f(self):
        if len(self.fofn[self.current_run]) == 1:
            return(self.fofn[self.current_run][0])
        return(self.fofn[self.current_run])

    @property
    def popr(self):
        self._sig_popr = True
        return(self._setr[-1])

    @property
    def popf(self):
        self._sig_popr = True
        if len(self.fofn[self._setr[-1]]) == 1:
            return(self.fofn[self._setr[-1]][0])
        return(self.fofn[self._setr[-1]])

    # should be setter, but it sort of behaves differently
    def pushr(self):
        self._setr.append(self.current_run)

    @property
    def past(self):
        paths = [path.strip() for path in execute(['cat', os.path.join(self.logdir, 'output.fofn')],
                                                  return_out=True, silent=True)]
        return(list(enumerate(paths)))
    
    #---------------------------------------------------
    
    @property
    def ids(self):
        return([p.split('/')[-2] for p in self.fofn if p != ''])
    
    @property
    def outputs(self):
        return(self.metadata['outputs'])
    
    @property
    def outputs_list(self):
        return([v for k, v in self.metadata['outputs'].items()])
    
    @property
    def root(self):
        return(self.metadata['workflowRoot'])
