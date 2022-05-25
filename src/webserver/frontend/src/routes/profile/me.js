export async function patch(request) {
    let headers = request.headers;
    headers["content-type"] = "application/json"
    const response = await fetch('http://webserver-backend.default.svc.cluster.local/users/me', {
        method: 'PATCH',
        credentials: 'include',
        headers: headers,
        body: JSON.stringify(request.body)
    }).then(r => r.json());
    console.log(response);
    return {
        headers: response.headers,
        body: response.body
    }
}
