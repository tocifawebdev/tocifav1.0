<script setup>
import { ref, onMounted } from 'vue';
import { EditIcon } from 'vue-tabler-icons';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import { fetchMoneyManagementItems, updateMoneyManagementItem } from '@/_mockApis/components/moneymanagement/indexMoneymanagement'; // API untuk rekening
import { updateLockRekeningStatus } from '@/_mockApis/components/moneymanagement/indexLockLimitRekening'; 

const search = ref('');
const dialog = ref(false);
const headers = ref([
    { title: 'No', key: 'no', align: 'left' },
    { title: 'Rekening ID', key: 'id', align: 'left' },
    { title: 'Bank Name', key: 'product', align: 'left' },
    { title: 'Rekening Name', key: 'status', align: 'left' },
    { title: 'Rekening Number', key: 'price', align: 'left' },
    { title: 'Reckening Balance', key: 'rekening', align: 'left', sortable: false },
    { title: 'Actions', key: 'actions', align: 'left', sortable: false }
]);

const productlist = ref([]);
const editedItem = ref({
    id: '',
    product: '',
    status: '',
    price: '',
    rekening: ''
});
const editedIndex = ref(-1);
const dialogTitle = ref('');

async function fetchRekeningData() {
    try {
        const response = await fetchMoneyManagementItems(); 
        productlist.value = response.map(item => ({
            id: item.id,
            product: item.product,     // Bank Name
            status: item.status,       // Rekening Name
            price: item.price,         // Rekening Balance
            rekening: item.rekening,         // Rekening Balance
            isActive: item.isActive,   // Status lock (ON/OFF)
        }));
    } catch (error) {
        console.error('Failed to fetch rekening data:', error.message);
    }
}

// Fungsi untuk toggle lock/unlock rekening
async function toggleStatus(item) {
    try {
        const newStatus = !item.isActive;
        await updateLockRekeningStatus(newStatus); 
        item.isActive = newStatus; 
    } catch (error) {
        console.error('Failed to toggle status:', error.message);
        alert('Gagal mengubah status rekening.');
    }
}

function editItem(item) {
    editedIndex.value = productlist.value.indexOf(item);
    editedItem.value = { ...item };
    dialogTitle.value = 'Edit Rekening';
    dialog.value = true;
}

async function save() {
    try {
        if (editedIndex.value > -1) {
            await updateMoneyManagementItem({
                id: editedItem.value.id,
                product: editedItem.value.product,
                status: editedItem.value.status,
                price: editedItem.value.price,
                rekening: editedItem.value.rekening,
            });

            Object.assign(productlist.value[editedIndex.value], editedItem.value);
        }
        dialog.value = false; 
    } catch (error) {
        console.error('Failed to save rekening data:', error.message);
        alert('Gagal menyimpan perubahan rekening.');
    }
}

onMounted(() => {
    fetchRekeningData();
});
</script>

<template>
    <v-row>
        <v-col cols="12">
            <UiParentCard title="Money Management">
                <v-data-table
                    class="rounded-md datatabels productlist"
                    :headers="headers"
                    :items="productlist"
                    v-model:search="search"
                    items-per-page="5"
                    item-value="product"
                    color="primary"
                    hide-default-footer
                >
                    <template v-slot:item.no="{ index }">
                        <span class="text-subtitle-1 text-left">{{ index + 1 }}</span>
                    </template>
                    <template v-slot:item.id="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.id }}</span>
                    </template>
                    <template v-slot:item.product="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.product }}</span>
                    </template>
                    <template v-slot:item.status="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.status }}</span>
                    </template>
                    <template v-slot:item.price="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.price }}</span>
                    </template>
                    <template v-slot:item.rekening="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.rekening }}</span>
                    </template>
                    <template v-slot:item.actions="{ item }">
                        <div class="d-flex gap-2 justify-left align-center">
                            <EditIcon
                                height="20"
                                width="20"
                                class="text-primary cursor-pointer"
                                size="small"
                                @click="editItem(item)"
                            />
                            <button
                                :class="['toggle-button', { active: item.isActive }]"
                                @click="toggleStatus(item)"
                            >
                                {{ item.isActive ? 'ON' : 'OFF' }}
                            </button>
                        </div>
                    </template>
                </v-data-table>
            </UiParentCard>
        </v-col>
        <!-- Dialog untuk edit data rekening -->
        <v-dialog v-model="dialog" max-width="500px">
            <v-card>
                <v-card-title>{{ dialogTitle }}</v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedItem.product"
                                    label="Bank Name"
                                    outlined
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedItem.status"
                                    label="Rekening Name"
                                    outlined
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedItem.price"
                                    label="Rekening Number"
                                    outlined
                                    type="number"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedItem.rekening"
                                    label="Rekening Balance"
                                    outlined
                                    type="number"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="error" text @click="dialog = false">Cancel</v-btn>
                    <v-btn color="primary" text @click="save">Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<style scoped>
.toggle-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 30px;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    color: white;
    background-color: #d9534f; /* OFF: Merah */
    transition: background-color 0.3s ease;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
}

.toggle-button.active {
    background-color: #5cb85c; /* ON: Hijau */
}

.toggle-button:focus {
    outline: none;
}
</style>
