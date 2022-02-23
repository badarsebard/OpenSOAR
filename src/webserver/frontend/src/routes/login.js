import "@kubernetes/client-node"
import {CoreV1Api, KubeConfig} from "@kubernetes/client-node";

export async function post(request) {
    let credentials = request.body;
    let headers = request.headers;
    headers["content-type"] = "application/x-www-form-urlencoded"
    if (!request.locals.jwt) {
        const body = await fetch('http://webserver-backend.default.svc.cluster.local/auth/jwt/login', {
            method: 'POST',
            credentials: 'include',
            headers: headers,
            body: `username=${encodeURIComponent(credentials.email)}&password=${encodeURIComponent(credentials.password)}`
        }).then((r) => r.json());
        if (!body.access_token) {
            return {status: 400, body};
        }
        headers['Authorization'] = `Bearer ${body.access_token}`
        const user = await fetch('http://webserver-backend.default.svc.cluster.local/users/me', {
            method: 'GET',
            credentials: 'include',
            headers: headers
        }).then((r) => r.json());
        delete user.incidents;
        let user_cookie = btoa(JSON.stringify(user));

        const kc = new KubeConfig();
        kc.loadFromCluster();
        const k8sApi = kc.makeApiClient(CoreV1Api);
        let argoServiceAccount = await k8sApi.readNamespacedServiceAccount("argo", "argo");
        let secretName = argoServiceAccount.body.secrets[0].name;
        let secret = await k8sApi.readNamespacedSecret(secretName, "argo");
        let tokenB64 = secret.body.data.token;
        let token = atob(tokenB64);

        let cookies;
        if (user.is_superuser) {
            cookies = [
                `jwt=${body.access_token}; HttpOnly; Max-Age=3600; Path=/; SameSite=lax; Secure`,
                `opensoar_user=${user_cookie}; Max-Age=3600; Path=/; SameSite=lax; Secure`,
                `authorization=Bearer ${token}; HttpOnly; Path=/argo/; SameSite=lax; Secure`,
            ]
        } else {
            cookies = [
                `jwt=${body.access_token}; HttpOnly; Max-Age=3600; Path=/; SameSite=lax; Secure`,
                `opensoar_user=${user_cookie}; Max-Age=3600; Path=/; SameSite=lax; Secure`,
            ]
        }
        return {
            headers: {
                'set-cookie': cookies
            },
            body: {
                "user": user,
                "jwt": body.access_token,
                "argo": token,
            }
        }
    }
    return {};
}
