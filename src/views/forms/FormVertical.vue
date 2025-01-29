<script setup lang="ts">
import { ref } from 'vue';
// common components
import BaseBreadcrumb from '@/components/shared/BaseBreadcrumb.vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UiChildCard from '@/components/shared/UiChildCard.vue';

//Components
import BasicLayout from '@/components/forms/form-vertical/BasicLayout.vue';
import BasicWithIcons from '@/components/forms/form-vertical/BasicWithIcons.vue';
import FormSeprator from '@/components/forms/form-vertical/FormSeprator.vue';
import Collapsible from '@/components/forms/form-vertical/Collapsible.vue';
import PersonalInfoTab from '@/components/forms/form-vertical/PersonalInfoTab.vue';
import AccountDetailsTab from '@/components/forms/form-vertical/AccountDetailsTab.vue';
import SocialLinksTab from '@/components/forms/form-vertical/SocialLinksTab.vue';

/*tab*/
/*tab*/
const tab = ref(null);

// theme breadcrumb
const page = ref({ title: 'Upload Item' });
const breadcrumbs = ref([
    {
        text: 'Dashboard',
        disabled: false,
        href: '#'
    },
    {
        text: 'Upload Item',
        disabled: true,
        href: '#'
    }
]);
</script>

<template>
   <BaseBreadcrumb :title="page.title" :breadcrumbs="breadcrumbs"></BaseBreadcrumb>
   <v-row>
        <!-- <v-col cols="12" md="6">
            <UiParentCard title="Basic Layout">
                <BasicLayout/>
            </UiParentCard>           
        </v-col>
        <v-col cols="12" md="6">
            <UiParentCard title="Basic with Icons">
                <BasicWithIcons/>
            </UiParentCard>           
        </v-col>
        <v-col cols="12">
            <FormSeprator/>        
        </v-col>
        <v-col cols="12">
            <Collapsible/>        
        </v-col> -->
        <v-col cols="12">
            <UiParentCard title="Upload Item" class="mt-6">
            <PersonalInfoTab/>
            </UiParentCard>
        </v-col>
   </v-row>           
</template>
