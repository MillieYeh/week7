// GET
function submit_entry(){
    let list = document.getElementById("list");
    let username = document.getElementById("username").value;
    let src = `/api/member?username=${username}`;
    fetch(src).then((response) => {
        return response.json();
    }).then((result) => {
        if(result.data != null) {
            list.innerHTML = result.data.name + ' ' + '(' +result.data.username + ')';
        }
        else {
            list.innerHTML = '無此帳戶';
        }
    });
};

// PATCH
function update_entry(){
    let list2 = document.getElementById("list2");
    let updatename = document.getElementById("updatename").value;
    let src = "http://127.0.0.1:3000/api/member";
    fetch(src, {
        method: "PATCH",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "name": updatename
        })
    }).then((response) => {
        return response.json();
    }).then((result) => {
        console.log('result: ', result);
        list2.innerHTML = '更新成功';
    }).catch((error) => {
        console.log('error: ', error);
        list2.innerHTML = '更新失敗';
    })
}
