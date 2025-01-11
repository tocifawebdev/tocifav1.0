<script setup>
import { ref, computed, onMounted } from 'vue';
import { EditIcon, TrashIcon } from 'vue-tabler-icons';
import UiParentCard from '@/components/shared/UiParentCard.vue';
// Simulasi fungsi API, jika Anda ingin tetap mempertahankan struktur
// import { addVendor, updateVendor, deleteVendor } from '@/_mockApis/apps/ecommerce/indexVendor';

const search = ref('');
const dialog = ref(false);
const dialogDelete = ref(false);
const headers = ref([
    { title: 'No', key: 'no', align: 'left' },
    { title: 'Id PO', key: 'id', align: 'left' },
    { title: 'Purchase Date', key: 'product', align: 'left' },
    { title: 'Vendor Name', key: 'product', align: 'left' },
    { title: 'Vendor Address', key: 'product', align: 'left', sortable: false },
    { title: 'Vendor Phone Number', key: 'product', align: 'left' },
    { title: 'Item Name', key: 'product', align: 'left' },
    { title: 'Item Description', key: 'product', align: 'left' },
    { title: 'Item Price', key: 'product', align: 'left' },
    { title: 'Total Items', key: 'product', align: 'left', sortable: false },
    { title: 'Total Prices', key: 'product', align: 'left' },
    { title: 'Payment Method', key: 'product', align: 'left' },
    { title: 'Payment Status', key: 'paymentStatus', align: 'left' },
    { title: 'Recipe Status', key: 'recipeStatusFile', align: 'left' },
    { title: 'Admin Id', key: 'product', align: 'left' },
    { title: 'Admin Notes', key: 'product', align: 'left', sortable: false },
    { title: 'Verification Status', key: 'verificationStatus', align: 'left' },
    { title: 'Verification Date', key: 'product', align: 'left' },
    { title: 'Verified By', key: 'product', align: 'left' },
    { title: 'Verified Notes', key: 'verifiednotes', align: 'left' },
    { title: 'Actions', key: 'actions', align: 'left', sortable: false }
]);

const productlist = ref([
    {
        id: 'V001',
        product: 'Printer Ink',
        status: 'In Stock',
        price: '120000',
        rekening: '1234567890',
        paymentStatus: 'Paid',
        verificationStatus: 'Verified',
        recipeStatusFile: 'Photo',
        verifiednotes: 'Hello Man!!!',
    },
    {
        id: 'V002',
        product: 'Paper A4',
        status: 'Out of Stock',
        price: '250000',
        rekening: '9876543210',
        paymentStatus: 'Paid',
        verificationStatus: 'Verified',
        recipeStatusFile: 'Photo',
        verifiednotes: 'Hello Man!!!',
    },
    {
        id: 'V003',
        product: 'Office Chair',
        status: 'In Stock',
        price: '750000',
        rekening: '1122334455',
        paymentStatus: 'Paid',
        verificationStatus: 'Verified',
        recipeStatusFile: 'Photo',
        verifiednotes: 'Hello Man!!!',
    },
]);

const editedIndex = ref(-1);
const editedItem = ref({
    id: '',
    product: '',
    status: '',
    price: '',
    rekening: '',
    paymentStatus: '', // Properti baru untuk Payment Status
    verificationStatus: '', // Properti baru untuk Verification Status
    recipeStatusFile: null, // Properti baru untuk Recipe File
    verifiednotes: ''
});
const defaultItem = {
    id: '',
    product: '',
    status: '',
    price: '',
    rekening: '',
    verifiednotes: ''
};

const formTitle = computed(() => (editedIndex.value === -1 ? 'New Item SO' : 'Edit History Request PO'));

function editItem(item) {
    editedIndex.value = productlist.value.indexOf(item);
    editedItem.value = { ...item };
    dialog.value = true;
}

async function deleteItem(item) {
    editedIndex.value = productlist.value.indexOf(item);
    editedItem.value = { ...item };
    dialogDelete.value = true;
}

async function deleteItemConfirm() {
    try {
        productlist.value.splice(editedIndex.value, 1);
        closeDelete();
    } catch (error) {
        console.error('Failed to delete vendor:', error);
    }
}

function close() {
    dialog.value = false;
    Object.assign(editedItem.value, defaultItem);
    editedIndex.value = -1;
}

function closeDelete() {
    dialogDelete.value = false;
    Object.assign(editedItem.value, defaultItem);
    editedIndex.value = -1;
}

async function save() {
    try {
        if (editedIndex.value > -1) {
            Object.assign(productlist.value[editedIndex.value], editedItem.value);
        } else {
            const newVendor = { ...editedItem.value };
            newVendor.id = `V00${productlist.value.length + 1}`; // Generate simple ID
            productlist.value.push(newVendor);
        }
        close();
    } catch (error) {
        console.error('Failed to save vendor:', error);
    }
}

onMounted(() => {
    console.log('Dummy data loaded:', productlist.value);
});
</script>


<template>
    <v-row>
        <v-col cols="12">
            <UiParentCard title="History Request PO">
                <v-data-table
                    class="rounded-md datatabels productlist"
                    :headers="headers"
                    :items="productlist"
                    v-model:search="search"
                    items-per-page="5"
                    item-value="product"
                    color="primary"
                >
                    <!-- Kolom No -->
                    <template v-slot:item.no="{ index }">
                        <span class="text-subtitle-1 text-left">{{ index + 1 }}</span>
                    </template>
                    <!-- Kolom ID -->
                    <template v-slot:item.id="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.id }}</span>
                    </template>
                    <!-- Kolom Name -->
                    <template v-slot:item.product="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.product }}</span>
                    </template>
                    <!-- Kolom Unit -->
                    <template v-slot:item.status="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.status }}</span>
                    </template>
                    <!-- Kolom Actions -->
                    <template v-slot:item.actions="{ item }">
                        <div class="d-flex gap-2 justify-left">
                            <EditIcon
                                height="20"
                                width="20"
                                class="text-primary cursor-pointer"
                                size="small"
                                @click="editItem(item)"
                            />
                            <TrashIcon
                                height="20"
                                width="20"
                                class="text-error cursor-pointer"
                                size="small"
                                @click="deleteItem(item)"
                            />
                        </div>
                    </template>
                    <template v-slot:top>
                        
                        <v-toolbar class="bg-surface" flat>
                            <v-dialog v-model="dialog" max-width="500px">
                                <template v-slot:activator="{ props }">
                                    <div class="d-md-flex block justify-space-between w-100 pb-6 align-left">
                                        <v-text-field
                                            v-model="search"
                                            append-inner-icon="mdi-magnify"
                                            label="Search"
                                            single-line
                                            hide-details
                                            class="mb-md-0 mb-3"
                                        />
                                        <div class="export-icons">
                                            <!-- Ikon PDF -->
                                            <i
                                                class="bi bi-file-earmark-pdf text-danger icon"
                                                title="Export to PDF"
                                                @click="exportToPDF"
                                            ></i>
                                            <!-- Ikon Excel -->
                                            <i
                                                class="bi bi-file-earmark-excel text-success icon"
                                                title="Export to Excel"
                                                @click="exportToExcel"
                                            ></i>
                                        </div>
                                        <!-- <v-btn color="primary" variant="flat" dark v-bind="props">Add New Item SO</v-btn> -->
                                    </div>
                                </template>
                                <v-card>
                                    <v-card-title class="pa-4 bg-primary">
                                        <span class="text-h5">{{ formTitle }}</span>
                                    </v-card-title>
                                    <v-card-text>
                                        <v-container class="px-0">
                                            <v-row>
                                                <!-- Item Name -->
                                                <v-col cols="12">
                                                    <v-select
                                                        v-model="editedItem.paymentStatus"
                                                        :items="['Paid', 'Unpaid']"
                                                        label="Payment Status"
                                                        placeholder="Select Payment Status"
                                                    ></v-select>
                                                </v-col>
                                                <v-col cols="12">
                                                    <v-select
                                                        v-model="editedItem.verificationStatus"
                                                        :items="['Verified', 'Unverified']"
                                                        label="Verification Status"
                                                        placeholder="Select Verification Status"
                                                    ></v-select>
                                                </v-col>
                                                <v-col cols="12">
                                                    <v-label class="mb-2 font-weight-medium">Verified Notes</v-label>
                                                    <v-text-field
                                                    v-model="editedItem.verifiednotes"
                                                    label=""
                                                    placeholder="Verified Notes"
                                                    variant="outlined"
                                                    color="primary"
                                                    ></v-text-field>
                                                </v-col>
                                                <v-col cols="12">
                                                    <v-file-input
                                                        v-model="editedItem.recipeStatusFile"
                                                        label="Recipe Status"
                                                        placeholder="Upload Recipe File"
                                                        show-size
                                                        accept=".pdf,.jpg,.png"
                                                    ></v-file-input>
                                                </v-col>
                                            </v-row>
                                        </v-container>
                                    </v-card-text>
                                    <v-card-actions>
                                        <v-spacer></v-spacer>
                                        <v-btn color="error" variant="flat" dark @click="close">Cancel</v-btn>
                                        <v-btn color="primary" variant="flat" dark @click="save">Save</v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-dialog>
                            <v-dialog v-model="dialogDelete" max-width="500px">
                                <v-card>
                                    <v-card-title class="text-h5 text-left py-6">Are you sure you want to delete this item?</v-card-title>
                                    <v-card-actions>
                                        <v-spacer></v-spacer>
                                        <v-btn color="error" variant="flat" dark @click="closeDelete">Cancel</v-btn>
                                        <v-btn color="primary" variant="flat" dark @click="deleteItemConfirm">OK</v-btn>
                                        <v-spacer></v-spacer>
                                    </v-card-actions>
                                </v-card>
                            </v-dialog>
                        </v-toolbar>
                    </template>
                    <template v-slot:no-data>
                        <v-btn color="primary" @click="initialize">Reset</v-btn>
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
    width: 50px; /* Lebar tombol lebih kecil */
    height: 25px; /* Tinggi tombol lebih kecil */
    border: none;
    border-radius: 12.5px; /* Sesuai tinggi tombol untuk membuat bentuk oval */
    cursor: pointer;
    font-size: 12px; /* Ukuran font lebih kecil */
    font-weight: bold;
    color: white;
    background-color: #d9534f; /* Default warna OFF (merah) */
    transition: background-color 0.3s ease;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
}

.toggle-button.active {
    background-color: #5cb85c; /* Warna ON (hijau) */
}

.toggle-button:focus {
    outline: none;
}

.export-icons {
    display: flex;
    justify-content: flex-end; /* Ikon berada di kanan */
    gap: 10px; /* Jarak antar ikon */
    margin-bottom: 7px; /* Ruang di bawah ikon */
    margin-top: 7px; /* Ruang di bawah ikon */
}

.icon {
    font-size: 1.5rem; /* Ukuran ikon */
    cursor: pointer;
    transition: opacity 0.3s ease;
}

.icon:hover {
    opacity: 0.8; /* Efek hover */
}
</style>


