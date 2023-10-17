/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

// function main(params) {

//     const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
//     const cloudant = CloudantV1.newInstance({
//       authenticator: authenticator
//     });
//     cloudant.setServiceUrl(params.COUCH_URL);
//     console.log(cloudant);

//     let dbListPromise = getDbs(cloudant);
//     return dbListPromise;
// }
function main(params) {
    const cloudant = CloudantV1.newInstance({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });
    let dbListPromise = getDbs(cloudant);
    return dbListPromise;
}

// function getDbs(cloudant) {
//      return new Promise((resolve, reject) => {
//          cloudant.getAllDbs()
//              .then(body => {
//                  resolve({ dbs: body.result });
//              })
//              .catch(err => {
//                   console.log(err);
//                  reject({ err: err });
//              });
//      });
//  }
 function getDbs(cloudant) {
    return new Promise((resolve, reject) => {
        cloudant.db.list()
            .then(body => {
                resolve({ dbs: body });
            })
            .catch(err => {
                reject({ err: err });
            });
    });
}

 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }
 main({
    "COUCH_URL": "https://1223dee1-c3da-4e4a-84db-40df919d7208-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "Av_BspR8cYuy4Ud9Aek4I6geXIuQ2mwHoeFEXsC0nfoY"
})