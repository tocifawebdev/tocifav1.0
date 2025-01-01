import { defineStore } from 'pinia';
import { fetchWrapper } from '@/utils/helpers/fetch-wrapper';
import { router } from '@/router';

const baseUrl = 'http://127.0.0.1:8080';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        user: JSON.parse(localStorage.getItem('user') || 'null'), // Save User and Token
    }),
    actions: {
        async login(userid: string, password: string) {
            try {
                const user = await fetchWrapper.post(`${baseUrl}/login/`, { userid, password });
                
                if (!user || !user.token) {
                    throw new Error('Invalid login response from server');
                }

                this.user = user;

                // Save User and Token in local storage
                localStorage.setItem('user', JSON.stringify(user));

                // Redirect page
                router.push('/dashboards/modern');
            } catch (error: any) {
                console.error(error);
                throw new Error(error?.message || 'Invalid login credentials');
            }
        },
        logout() {
            this.user = null;

            // Delete user data dari local storage
            localStorage.removeItem('user');

            // Redirect to login page
            router.push('/login');
        },
    },
});
