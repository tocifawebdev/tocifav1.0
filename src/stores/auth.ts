import { defineStore } from 'pinia';
import { router } from '@/router';
import { fetchWrapper } from '@/utils/helpers/fetch-wrapper';

const baseUrl = `${import.meta.env.VITE_API_URL}/login`;

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        user: JSON.parse(localStorage.getItem('user') || 'null'),
        returnUrl: null
    }),
    actions: {
        async login(userid: string, password: string) {
            try {
                // Mengirimkan POST request ke endpoint login
                const response = await fetchWrapper.post(baseUrl, { userid, password });
                
                // update pinia state dengan data user
                this.user = response.user;

                // Menyimpan user details di local storage
                localStorage.setItem('user', JSON.stringify(response.user));

                // Redirect ke halaman sebelumnya atau default dashboard
                router.push(this.returnUrl || '/dashboards/modern');
            } catch (error: any) {
                throw error?.message || 'Login failed';
            }
        },
        logout() {
            this.user = null;
            localStorage.removeItem('user');
            router.push('/');
        }
    }
});
