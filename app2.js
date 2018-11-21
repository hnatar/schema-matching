'use strict'

const express = require('express')
const fs = require('fs')
const MongoClient = require('mongodb').MongoClient

const fetch_documents = (url, db, coll, field, callback) => {

    MongoClient.connect(url, function(err, client) {
        if(err) {
            console.log('MongoClient: Cannot connect to Mongo')
            process.exit()
        }
        const collection = client.db(db).collection(coll)
        console.log('field=', field)
        let P = {_id: 0}
        if(field) P[field] = 1
        else P = {}
        collection.find({}).project(P).toArray( (err, docs) => {
            if(err) {
                console.log('MongoClient: Error during query')
                process.exit()
            }
            console.log('serviced request')
            callback(docs)
            client.close()
        })
    })

}

const app = express()

app.get('/collections/:db/', (req,res) => {
    MongoClient.connect('mongodb://127.0.0.1:27018/', function(err, client) {
        if(err) {
            console.log('MongoClient: Cannot connect to Mongo')
            process.exit()
        }
        const db = client.db(req.params.db)
        const result = []
        db.listCollections({}).toArray( (err, docs) => {
            if(err) {
                console.log('MongoClient: Error during query')
                process.exit()
            }
            for(let doc of docs) {
                result.push( doc['name'] )
            }
            res.write('<table>\n')
            res.write(' <tr>\n')
            res.write('  <td><b>Use?</b></td>\n')
            res.write('  <td><b>Model Name</b></td>\n')
            res.write(' </tr>\n')
            for(let row of result) {
                res.write('<tr>\n')
                res.write('<td><a href="">[+]</a></td>\n')
                res.write(`<td>${row}</td>\n`)
            }
            res.write('</table>\n')
            res.end()
            // res.send( JSON.stringify(result) )
            client.close()
        })
    })
})

app.get('/models', (req,res) => {
    fs.readdir('Backend/FieldData/', (err, files) => {
        if(err) {
            console.log("Request error: Could not read model directory")
            process.exit()
        }
        res.write('<table>\n')
        res.write(' <tr>\n')
        res.write('  <td><b>Use?</b></td>\n')
        res.write('  <td><b>Model Name</b></td>\n')
        res.write(' </tr>\n')
        files.forEach( file => {
            res.write('<tr>\n')
            let Path = 'Backend/FieldData/' + file
            res.write(`<td><a data-path="${Path}" href="">[+]</a></td>\n`)
            res.write(`<td>${file}</td>\n`)
            res.write('</tr>\n')
        })
        res.write('</table>\n')
        res.end()
    })
})

app.get('/fetch/:db?/:collection?/:field?', (req, res) => {
    let db = req.params.db || 'EDM'
    let port = 27018
    let collection = req.params.collection || 'baddriverreports'
    let field = req.params.field || undefined

    fetch_documents(`mongodb://localhost:${port}/`, db, collection, field, (docs) => {
        console.log(docs)
        let table = {}
        let keys = new Set()
        for(let doc of docs) {
            for(let k_i in doc) {
                if(keys.has(k_i)) continue;
                keys.add(k_i)
            }
        }
        let Path = '/' + db + '/' + collection + '/'
        res.write('<table>\n')
        res.write(' <tr>\n')
        keys.forEach( (k) => {
            res.write(  `<td><b>${k}</b><a data-path="${Path+k}">[+]</a></td>\n` )
        })
        res.write(' </tr>\n')
        for(let doc of docs) {
            let Row = {}
            for(let k in keys) {
                Row[k] = '-'
            }
            for(let k_i in doc) {
                Row[k_i] = doc[k_i]
            }
            res.write(' <tr>\n')
            keys.forEach( (k)=> {
                res.write(`  <td>${Row[k]}</td>\n`)
            })
            res.write(' </tr>\n')
        }
        res.write('</table>\n')
        res.end()
    })

})

const port = 4000
app.listen(port, () => {
    console.log(`Express: Listening for requests on port ${port}`)
})

