import { createRouter, createWebHistory } from 'vue-router';
import MainRoutes from './MainRoutes';
import AuthRoutes from './AuthRoutes';
import { useAuthStore } from '@/stores/auth';

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/:pathMatch(.*)*',
            component: () => import('@/views/authentication/Error.vue')
        },
        MainRoutes,
        AuthRoutes
    ]
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    const publicPages = ['/auth/login'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = !!authStore.user;

    if (authRequired && !loggedIn) {
        return next('/auth/login');
    }

    next();
})
