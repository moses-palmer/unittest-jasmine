// Read command line options
var projectBaseDir = process.argv[1];
var options = JSON.parse(process.argv[2]);
var specFiles = process.argv.slice(3);


// Create and initialise a runner
var jrunner = new (require("jasmine"))({
    projectBaseDir: projectBaseDir
});
jrunner.loadConfig(options);
jrunner.addSpecFiles(specFiles);


// Remove default logging
jrunner.configureDefaultReporter({
    print: function() {}
});


// Add a custom reporter
reporter = {};
["suiteStarted", "suiteDone", "specStarted", "specDone"].forEach(
    function(event) {
        reporter[event] = function(data) {
            console.log(JSON.stringify({
                event: event,
                data: data
            }));
        };
    });
jrunner.jasmine.getEnv().addReporter(reporter);


jrunner.execute();
