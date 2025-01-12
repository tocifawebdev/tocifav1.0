<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// common components
import BaseBreadcrumb from '@/components/shared/BaseBreadcrumb.vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';

//Table
import EditableTable from '@/components/table/Table1.vue';

const router = useRouter();

// theme breadcrumb
const page = ref({ title: 'User Management' });
const breadcrumbs = ref([
    {
        text: 'Dashboard',
        disabled: false,
        href: '#',
        action: () => {
            router.push('/dashboards/modern');
        },
    },
    {
        text: 'User Management',
        disabled: true,
        href: '#'
    }
]);
</script>

<template>
    <!-- ---------------------------------------------------- -->
    <!-- Table Editable -->
    <!-- ---------------------------------------------------- -->
    <BaseBreadcrumb :title="page.title" :breadcrumbs="breadcrumbs" />
    <v-row>
        <v-col cols="12">
            <UiParentCard title="List User">
                <EditableTable />
            </UiParentCard>
        </v-col>
    </v-row>
</template>
