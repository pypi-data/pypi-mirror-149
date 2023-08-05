version 1.0

workflow HelloInput {
    input {
        String name = 'blah'
    }
    call WriteGreeting {
        input: name = name
    }

    output {
        File response = WriteGreeting.response
    }
}

task WriteGreeting {
    input {
        String name
    }

    # specify parameter value (name) in `input.json` file
    command <<<
        echo "hello ~{name}!" > hello.txt
    >>>

    output {
        File response = 'hello.txt'
    }

    runtime {
        docker: 'ubuntu:latest'
    }
}