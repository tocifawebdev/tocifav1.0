<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { Form } from 'vee-validate';

/* Social icons */
import google from '@/assets/images/svgs/google-icon.svg';
import facebook from '@/assets/images/svgs/facebook-icon.svg';

/* Form state */
const checkbox = ref(false);
const valid = ref(false);
const show1 = ref(false);
const password = ref('');
const userid = ref('');
const passwordRules = ref([
    (v: string) => !!v || 'Password is required',
    (v: string) => (v && v.length <= 20) || 'Password must be less than 20 characters'
]);
const useridRules = ref([(v: string) => !!v || 'UserID is required']);

function validate(values: any, { setErrors }: any) {
    const authStore = useAuthStore();
    return authStore.login(userid.value, password.value).catch((error) => setErrors({ apiError: error }));
}
</script>

<template>
    <Form @submit="validate" v-slot="{ errors, isSubmitting }" class="mt-3">
        <v-label class="text-subtitle-1 font-weight-semibold pb-2 text-lightText">UserID</v-label>
        <VTextField
            v-model="userid"
            :rules="useridRules"
            class="mb-8"
            required
            hide-details="auto"
        ></VTextField>
        <v-label class="text-subtitle-1 font-weight-semibold pb-2 text-lightText">Password</v-label>
        <VTextField
            v-model="password"
            :rules="passwordRules"
            required
            hide-details="auto"
            type="password"
            class="pwdInput"
        ></VTextField>
        <div class="d-flex flex-wrap align-center my-3 ml-n2">
            <v-checkbox v-model="checkbox" hide-details color="primary">
                <template v-slot:label>Remember this Device</template>
            </v-checkbox>
        </div>
        <v-btn size="large" :loading="isSubmitting" color="primary" :disabled="valid" block type="submit" flat>
            Sign In
        </v-btn>
        <div v-if="errors.apiError" class="mt-2">
            <v-alert color="error">{{ errors.apiError }}</v-alert>
        </div>
    </Form>
</template>
