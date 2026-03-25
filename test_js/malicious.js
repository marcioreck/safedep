function riskyFunction() {
    eval("console.log('Malicious code')");
    const exec = require('child_process').exec;
    exec('rm -rf /');
}

riskyFunction();
