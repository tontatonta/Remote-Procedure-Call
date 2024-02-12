const net = require("net")
const server_address = "./rpc_file"

const client = new net.Socket()

const request = {
    "method": "",
    "params": "",
    "id": ""
};


function readUser(question) {
    const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
    });

    return new Promise((resolve) => {
        readline.question(question, (answer) => {
            resolve(answer);
            readline.close();
        });
    });
}


(async function main() {

    method = await readUser('方法を入力してください --> ');
    params = await readUser('数値を入力してください --> ');
    id = await readUser('IDを入力してください --> ');

    request.method = method == ""? request.method : method;
    request.params = params == ""? request.params : params;
    request.id = id == ""? request.id : id;
   
    client.connect(server_address, () => {
        console.log('サーバと接続');
        
        
        client.write(JSON.stringify(request));
    });
    
    client.on('data', (data) => {
        const response = JSON.parse(data);
        
        if (response.error) {
            console.error('Error:', response.error);
        }else{
            console.log('結果 -->');
            console.log(response.結果);
            console.log('ID -->');
            console.log(response.ID);
        }
        
        
    });
    client.on('close', () => {
        console.log('Connection closed');
    });
    client.on('error', (error) => {
        console.error('Error:', error);
    });
    
})();