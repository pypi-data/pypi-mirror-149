version 1.0

import "hello-world-swf-sub.wdl" as WG

workflow HelloInput {
    input {
        String name
    }
    call WG.WriteGreeting {
        input: name = name
    }
}