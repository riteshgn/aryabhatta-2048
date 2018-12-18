'use strict';

const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
    console.log(`Master ${process.pid} is running`);

    for (let i=0; i<numCPUs; i++) {
        cluster.fork();
    }

    cluster.on('exit', (worker) => {
        console.log(`worker ${worker.process.pid} died`);
    });
} else {

    const restify = require('restify');

    const oracle = require('./ai_oracle');

    const server = restify.createServer();
    server.use(restify.plugins.bodyParser());
    server.post('/oracle/play', play);
    server.post('/oracle/empty_cells', emptyCells);
    server.post('/oracle/available_moves', availableMoves);

    server.listen(18080, function() {
        console.log('[pid: %s] %s listening at %s', process.pid, server.name, server.url);
    });

    ///////////////////////////////////////////////////////////////////////////////////

    function emptyCells(req, res, next) {
        res.send(200, {positions: oracle.emptyCells(req.body.state)});
        next();
    }

    function availableMoves(req, res, next) {
        const moves = oracle.availableMoves(req.body.state);
        res.send(200, {moves});
        next();
    }

    function play(req, res, next) {
        const state = oracle.play(req.body.state, req.body.choice);
        res.send(200, {state});
        next();
    }

}