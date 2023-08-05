version 1.0

task WriteGreeting {
    input {
        String name
    }

    # specify parameter value (name) in `input.json` file
    command <<<
        echo "hello ~{name}!"
    >>>
    
    output {
        File response = stdout()
    }

    runtime {
        docker: 'ubuntu:latest'
    }
}