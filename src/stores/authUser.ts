import { defineStore } from 'pinia';
import { fetchWrapper } from '@/utils/helpers/fetch-wrapper';

const baseUrl = 'http://127.0.0.1:8080/users';

export const useUsersStore = defineStore({
    id: 'Authuser',
    state: () => ({
        users: null as null | { loading: boolean } | { error: string } | Array<any>,
    }),
    actions: {
        async getAll() {
            this.users = { loading: true };
            try {
                const users = await fetchWrapper.get(baseUrl);
                this.users = users;
            } catch (error: unknown) {
                const errorMessage = (error as Error).message || 'Failed to fetch users';
                this.users = { error: errorMessage };
            }
        },
    },
});
