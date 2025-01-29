<script setup>
import { ref, onMounted } from 'vue';
import { EditIcon } from 'vue-tabler-icons';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import { fetchMoneyManagementItems, updateMoneyManagementItem } from '@/_mockApis/components/moneymanagement/indexMoneymanagement'; // API untuk data Money Management
import { updateLockRekeningStatus } from '@/_mockApis/components/moneymanagement/indexLockLimitRekening'; // API untuk Lock Rekening
import { fetchSummaryPOSO } from '@/_mockApis/components/moneymanagement/indexSummaryPOSO'; // API untuk rangkuman PO & SO
import dayjs from 'dayjs';

const search = ref('');
const dialog = ref(false);

// Header untuk tabel "Money Management"
const headers = ref([
    { title: 'No', key: 'no', align: 'left' },
    { title: 'Rekening ID', key: 'id', align: 'left' },
    { title: 'Bank Name', key: 'product', align: 'left' },
    { title: 'Rekening Name', key: 'status', align: 'left' },
    { title: 'Rekening Number', key: 'price', align: 'left' },
    { title: 'Piutang', key: 'receivables', align: 'left' },
    { title: 'Hutang', key: 'payables', align: 'left' },
    { title: 'Laba / Rugi', key: 'totalpayrec', align: 'left' },
    { title: 'Rekening Balance', key: 'rekening', align: 'left', sortable: false },
    { title: 'Actions', key: 'actions', align: 'left', sortable: false }
]);

// Header untuk tabel "Rangkuman PO & SO"
const headersSummaryPOSO = ref([
    { title: 'No', key: 'no', align: 'left' },
    { title: 'PO/SO ID', key: 'po_so_id', align: 'left' },
    { title: 'Order Date', key: 'order_date', align: 'left' },
    { title: 'Item Name', key: 'item_name', align: 'left' },
    { title: 'Item Price', key: 'item_price', align: 'left' },
    { title: 'Item Quantity', key: 'item_qty', align: 'left' },
    { title: 'Total Item Price', key: 'total_item_price', align: 'left' },
    { title: 'Payment Status', key: 'payment_status', align: 'left' },
    { title: 'Rekening Balance', key: 'rekening_balance', align: 'left' },
    { title: 'Add User', key: 'add_user', align: 'left' },
]);

const productlist = ref([]); // Data untuk Money Management
const summaryPOSOList = ref([]); // Data untuk Rangkuman PO & SO

function formatOrderDate(date) {
    return dayjs(date).format('YYYY-MM-DD hh:mm:ss A');
}

const editedItem = ref({
    id: '',
    product: '',
    status: '',
    price: '',
    rekening: ''
});
const editedIndex = ref(-1);
const dialogTitle = ref('');

// Fetch data Money Management
async function fetchRekeningData() {
    try {
        const response = await fetchMoneyManagementItems(); 
        productlist.value = response.map(item => ({
            id: item.id,
            product: item.product,     // Bank Name
            status: item.status,       // Rekening Name
            price: item.price,         // Nomor Rekening
            receivables: item.receivables,  // Piutang
            payables: item.payables,   // Hutang
            totalpayrec: item.totalpayrec,  // Total Piutang-Hutang
            rekening: item.rekening,   // Nominal Saldo Rekening
            isActive: item.isActive === "1",   // Status lock (ON/OFF)
        }));
    } catch (error) {
        console.error('Failed to fetch rekening data:', error.message);
    }
}

const loadSummaryPOSO = async () => {
    try {
        const data = await fetchSummaryPOSO(); // Panggil API
        console.log('Fetched Summary POSO Data:', data); // Pastikan data muncul di console
        summaryPOSOList.value = data; // Simpan data ke state
    } catch (error) {
        console.error('Failed to load summary POSO data:', error);
    }
};

// Fungsi untuk toggle lock/unlock rekening
async function toggleStatus(item) {
    try {
        // Tentukan status baru (true untuk ON, false untuk OFF)
        const newStatus = !item.isActive;

        // Panggil fungsi API untuk memperbarui status di server
        await updateLockRekeningStatus(newStatus);

        // Perbarui status di UI
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
    loadSummaryPOSO();
});
</script>

<template>
    <v-row>
        <!-- Tabel Money Management -->
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
                    <template v-slot:item.receivables="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.receivables }}</span>
                    </template>
                    <template v-slot:item.payables="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.payables }}</span>
                    </template>
                    <template v-slot:item.totalpayrec="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.totalpayrec }}</span>
                    </template>
                    <template v-slot:item.rekening="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.rekening }}</span>
                    </template>
                    <template v-slot:item.actions="{ item }">
                        <div class="d-flex gap-2 justify-center align-center">
                            <!-- Ikon edit -->
                            <EditIcon
                            height="20"
                            width="20"
                            class="text-primary cursor-pointer"
                            size="small"
                            @click="editItem(item)"
                            />

                            <!-- Tombol toggle -->
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
        <!-- Tabel Rangkuman PO & SO -->
        <v-col cols="12">
            <UiParentCard title="Rangkuman PO & SO">
                <v-data-table
                class="rounded-md datatabels summarylist"
                :headers="headersSummaryPOSO"
                :items="summaryPOSOList"
                items-per-page="5"
                color="primary"
                >
                    <template v-slot:item.no="{ index }">
                        <span>{{ index + 1 }}</span>
                    </template>
                    <template v-slot:item.po_so_id="{ item }">
                        <span>{{ item.po_so_id }}</span>
                    </template>
                    <template v-slot:item.order_date="{ item }">
                        <span class="text-subtitle-1 text-left">
                            {{ formatOrderDate(item.order_date) }}
                        </span>
                    </template>
                    <template v-slot:item.item_name="{ item }">
                        <ul>
                            <li v-for="name in item.item_name.split('|')" :key="name">{{ name }}</li>
                        </ul>
                    </template>
                    <template v-slot:item.item_price="{ item }">
                        <ul>
                            <li v-for="name in item.item_price.split('|')" :key="name">{{ name }}</li>
                        </ul>
                    </template>
                    <template v-slot:item.item_qty="{ item }">
                        <ul>
                            <li v-for="name in item.item_qty.split('|')" :key="name">{{ name }}</li>
                        </ul>
                    </template>
                    <template v-slot:item.total_item_price="{ item }">
                        <span>{{ item.total_item_price }}</span>
                    </template>
                    <template v-slot:item.payment_status="{ item }">
                        <span>{{ item.payment_status }}</span>
                    </template>
                    <template v-slot:item.rekening_balance="{ item }">
                        <span>{{ item.rekening_balance }}</span>
                    </template>
                    <template v-slot:item.add_user="{ item }">
                        <span>{{ item.add_user }}</span>
                    </template>
                </v-data-table>
            </UiParentCard>
        </v-col>
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