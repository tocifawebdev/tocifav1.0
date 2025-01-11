import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import { router } from './router';
import vuetify from './plugins/vuetify';
import '@/scss/style.scss';
import PerfectScrollbar from 'vue3-perfect-scrollbar';
import VueApexCharts from 'vue3-apexcharts';
import VueTablerIcons from 'vue-tabler-icons';
import 'vue3-carousel/dist/carousel.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import '@fortawesome/fontawesome-free/css/all.css';
import Maska from 'maska';

// i18n setup
import { createI18n } from 'vue-i18n';
import messages from '@/utils/locales/messages';

// ScrollTop
import VueScrollTo from 'vue-scrollto';

// LightBox
import VueEasyLightbox from 'vue-easy-lightbox';

// i18n Configuration
const i18n = createI18n({
    locale: 'en',
    messages: messages,
    silentTranslationWarn: true,
    silentFallbackWarn: true,
});

// Create Vue Application
const app = createApp(App);

// Remove `fakeBackend()` as it is no longer needed
// fakeBackend();

app.use(router);
app.use(PerfectScrollbar);
app.use(createPinia());
app.use(VueTablerIcons);
app.use(i18n);
app.use(Maska);
app.use(VueApexCharts);
app.use(vuetify).mount('#app');

// ScrollTop Use
app.use(VueScrollTo, {
    duration: 1000,
    easing: 'ease',
});

// Lightbox
app.use(VueEasyLightbox);