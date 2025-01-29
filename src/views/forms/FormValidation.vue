<script setup lang="ts">
import { ref } from 'vue';
import BaseBreadcrumb from '@/components/shared/BaseBreadcrumb.vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UiChildCard from '@/components/shared/UiChildCard.vue';
import FormSO from "@/components/forms/form-layouts/FormSO.vue";

const page = ref({ title: 'Form Request SO' });
const breadcrumbs = ref([
    {
        text: 'Dashboard',
        disabled: false,
        href: '#'
    },
    {
        text: 'Form Request SO',
        disabled: true,
        href: '#'
    }
]);

</script>
<template>
   <BaseBreadcrumb :title="page.title" :breadcrumbs="breadcrumbs"></BaseBreadcrumb>
   <v-row>
        <v-col cols="12">
             <UiParentCard title="Form Request SO" class="mt-6">
                <FormSO/>
             </UiParentCard>
        </v-col>
   </v-row>           
</template>