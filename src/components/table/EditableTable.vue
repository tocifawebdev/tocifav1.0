<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { fetchContacts, addContact, updateContact, deleteContact } from '@/_mockApis/apps/contact';

interface User {
    id: string;
    avatar: string;
    userinfo: string;
    usermail: string;
    phone: string;
    role: string;
    password: string;
    rolestatus: string;
}

const valid = ref(true);
const dialog = ref(false);
const search = ref('');
const rolesbg = ref(['Admin', 'Management']);
const baseUrl = import.meta.env.BASE_URL;
const adminAvatar = `${baseUrl}src/assets/images/profile/user-1.jpg`;
const managementAvatar = `${baseUrl}src/assets/images/profile/user-3.jpg`;
const desserts = ref<User[]>([]);
const editedIndex = ref(-1);
const editedItem = ref<User>({
  id: '',
  avatar: adminAvatar,
  userinfo: '',
  usermail: '',
  phone: '',
  jdate: '',
  role: 'Select Role',
  password: '',
  rolestatus: 'rgba(255, 0, 0, 0.2)',
});

onMounted(async () => {
    desserts.value = await fetchContacts();
});

const filteredList = computed(() =>
    desserts.value.filter((user) =>
        user.userinfo.toLowerCase().includes(search.value.toLowerCase())
    )
);

function editItem(item: User) {
    editedIndex.value = desserts.value.indexOf(item);
    editedItem.value = { ...item };
    dialog.value = true;
}

async function deleteItem(item: User) {
    if (confirm('Are you sure you want to delete this user?')) {
        try {
            await deleteContact(item.userinfo);
            desserts.value = await fetchContacts();
        } catch (error) {
            console.error('Failed to delete user:', error);
        }
    }
}

function close() {
    dialog.value = false;
    setTimeout(() => {
        editedItem.value = {
            id: '',
            avatar: adminAvatar,
            userinfo: '',
            usermail: '',
            phone: '',
            jdate: '',
            role: 'Admin',
            password: '123456',
            rolestatus: 'rgba(255, 0, 0, 0.2)',
        };
        editedIndex.value = -1;
    }, 300);
}

async function save() {
    try {
        if (editedIndex.value > -1) {
            await updateContact(editedItem.value);
        } else {
            await addContact(editedItem.value);
        }
        desserts.value = await fetchContacts();
        close();
    } catch (error) {
        console.error('Failed to save user:', error);
    }
}

const formTitle = computed(() => (editedIndex.value === -1 ? 'New User' : 'Edit User'));
</script>

<template>
    <v-row>
        <v-col cols="12" lg="4" md="6">
            <v-text-field
                density="compact"
                v-model="search"
                label="Search User"
                hide-details
                variant="outlined"
            ></v-text-field>
        </v-col>
        <v-col cols="12" lg="8" md="6" class="text-right">
            <v-dialog v-model="dialog" max-width="500">
                <template v-slot:activator="{ props }">
                    <v-btn color="primary" v-bind="props" flat class="ml-auto">
                        <v-icon class="mr-2">mdi-account-multiple-plus</v-icon>Add User
                    </v-btn>
                </template>
                <v-card>
                    <v-card-title class="pa-4 bg-secondary">
                        <span class="title text-white">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                        <v-form ref="form" v-model="valid" lazy-validation>
                            <v-row>
                                <v-col cols="12" sm="6">
                                    <v-text-field
                                        variant="outlined"
                                        hide-details
                                        v-model="editedItem.userinfo"
                                        label="Name"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-text-field
                                        variant="outlined"
                                        hide-details
                                        v-model="editedItem.usermail"
                                        label="User email"
                                        type="email"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-text-field
                                        variant="outlined"
                                        hide-details
                                        v-model="editedItem.password"
                                        label="Password"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-select
                                        variant="outlined"
                                        hide-details
                                        :items="rolesbg"
                                        v-model="editedItem.role"
                                        label="Role"
                                    ></v-select>
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-card-text>

                    <v-card-actions class="pa-4">
                        <v-spacer></v-spacer>
                        <v-btn color="error" @click="close">Cancel</v-btn>
                        <v-btn
                            color="secondary"
                            :disabled="editedItem.userinfo === '' || editedItem.usermail === ''"
                            variant="flat"
                            @click="save"
                        >Save</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-col>
    </v-row>
    <v-table class="mt-5">
        <thead>
            <tr>
                <th class="text-subtitle-1 font-weight-semibold">No</th>
                <th class="text-subtitle-1 font-weight-semibold">Name</th>
                <th class="text-subtitle-1 font-weight-semibold">ID</th>
                <th class="text-subtitle-1 font-weight-semibold">Password</th>
                <th class="text-subtitle-1 font-weight-semibold">Joining Date</th>
                <th class="text-subtitle-1 font-weight-semibold">Role</th>
                <th class="text-subtitle-1 font-weight-semibold">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(item, index) in filteredList" :key="item.id">
                <td class="text-subtitle-1">{{ index + 1 }}</td>
                <td>
                    <div class="d-flex align-center py-4">
                        <div>
                            <v-img :src="item.avatar" width="45px" class="rounded-circle img-fluid"></v-img>
                        </div>
                        <div class="ml-5">
                            <h4 class="text-h6 font-weight-semibold">{{ item.userinfo }}</h4>
                            <span class="text-subtitle-1 d-block mt-1 textSecondary">{{ item.usermail }}</span>
                        </div>
                    </div>
                </td>
                <td class="text-subtitle-1">{{ item.phone }}</td>
                <td class="text-subtitle-1">{{ item.password }}</td>
                <td class="text-subtitle-1">{{ item.jdate }}</td>
                <td>
                    <v-chip :style="{ backgroundColor: item.rolestatus }" size="small" label>
                        {{ item.role }}
                    </v-chip>
                </td>
                <td>
                    <div class="d-flex align-center">
                        <v-tooltip text="Edit">
                            <template v-slot:activator="{ props }">
                                <v-btn icon flat @click="editItem(item)" v-bind="props">
                                    <v-icon class="text-primary">mdi-pencil</v-icon>
                                </v-btn>
                            </template>
                        </v-tooltip>
                        <v-tooltip text="Delete">
                            <template v-slot:activator="{ props }">
                                <v-btn icon flat @click="deleteItem(item)" v-bind="props">
                                    <v-icon class="text-error">mdi-delete</v-icon>
                                </v-btn>
                            </template>
                        </v-tooltip>
                    </div>
                </td>
            </tr>
        </tbody>
    </v-table>
</template>