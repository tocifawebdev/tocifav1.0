<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { Form } from 'vee-validate';


const username = ref('');
const password = ref('');
const checkbox = ref(false);
const valid = ref(false);
const errorMessage = ref('');
const show1 = ref(false);

const emailRules = ref([(v: string) => !!v || 'ID is required']);
const passwordRules = ref([(v: string) => !!v || 'Password is required']);

const validate = async () => {
    const authStore = useAuthStore();
    try {
        await authStore.login(username.value, password.value); // Call Login
    } catch (error) {
        errorMessage.value = error;
    }
};
</script>

<template>
    <Form @submit="validate" v-slot="{ errors, isSubmitting }" class="mt-3">
        <v-label class="text-subtitle-1 font-weight-semibold pb-2 text-lightText">Username</v-label>
        <VTextField
            v-model="username"
            :rules="emailRules"
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
            <v-checkbox v-model="checkbox" :rules="[(v:any) => !!v || 'You must agree to continue!']" required hide-details color="primary">
                <template v-slot:label class="">Remember this Device</template>
            </v-checkbox>
        </div>
        <v-btn size="large" :loading="isSubmitting" color="primary" :disabled="valid" block type="submit" flat>Sign In</v-btn>
        <div v-if="errors.apiError || errorMessage" class="mt-2">
            <v-alert color="error">{{ errors.apiError || errorMessage }}</v-alert>
        </div>
    </Form>
    <v-row class="d-flex mb-3">
        <v-col cols="6" sm="6" style="visibility: hidden;">
            <v-btn variant="outlined" size="large" class="border text-subtitle-1" block>
                <img :src="google" height="16" class="mr-2" alt="google" />
                <span class="d-sm-flex d-none mr-1">Sign in with</span>Google
            </v-btn>
        </v-col>
        <v-col cols="6" sm="6" style="visibility: hidden;">
            <v-btn variant="outlined" size="large" class="border text-subtitle-1" block>
                <img :src="facebook" width="25" height="25" class="mr-1" alt="facebook" />
                <span class="d-sm-flex d-none mr-1">Sign in with</span>FB
            </v-btn>
        </v-col>
    </v-row>
    <div class="d-flex align-center text-center mb-3" style="visibility: hidden;">
        <div class="text-h6 w-100 px-5 font-weight-regular auth-divider position-relative">
            <span class="bg-surface px-5 py-3 position-relative">or sign in with</span>
        </div>  
    </div>
</template>
