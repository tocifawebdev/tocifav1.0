import { useAuthStore } from '@/stores/auth';

export const fetchWrapper = {
    get: request('GET'),
    post: request('POST'),
    put: request('PUT'),
    delete: request('DELETE'),
};

function request(method: string) {
    return (url: any, body?: any) => {
        const requestOptions: any = {
            method,
            headers: authHeader(url),
        };
        if (body) {
            requestOptions.headers['Content-Type'] = 'application/json';
            requestOptions.body = JSON.stringify(body);
        }
        return fetch(url, requestOptions).then(handleResponse);
    };
}

function authHeader(url: string) {
    const { user } = useAuthStore();
    const token = user?.token; // Get Token-state

    if (token) {
        return { Authorization: `Bearer ${token}` }; // Token Authorization
    }
    return {};
}

function handleResponse(response: any) {
    return response.text().then((text: any) => {
        const data = text && JSON.parse(text);

        if (!response.ok) {
            const { user, logout } = useAuthStore();
            if ([401, 403].includes(response.status) && user) {
                logout();
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}
