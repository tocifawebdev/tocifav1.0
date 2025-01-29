<script setup>
import { ref, computed, onMounted } from 'vue';
import { fetchRequestPOs, updateRequestPO, deleteRequestPO } from '@/_mockApis/apps/requestpo/indexRequestPo'; // Path ke file API
import dayjs from 'dayjs'; // Import Day.js

// State untuk menyimpan data dari API
const productlist = ref([]); // Data untuk tabel
const search = ref(''); // Search bar
const dialogDelete = ref(false);
const updateDialog = ref(false);

// Header untuk v-data-table
const headers = ref([
  { title: 'No', key: 'no', align: 'left' },
  { title: 'Id PO', key: 'id', align: 'left' },
  { title: 'Purchase Date', key: 'orderDate', align: 'left' },
  { title: 'Vendor Name', key: 'vendorName', align: 'left' },
  { title: 'Vendor Address', key: 'vendorAddress', align: 'left' },
  { title: 'Vendor Phone', key: 'vendorPhone', align: 'left' },
  { title: 'Item Name', key: 'itemName', align: 'left' },
  { title: 'Item Description', key: 'itemDesc', align: 'left' },
  { title: 'Item Price / Unit', key: 'itemPrice', align: 'left' },
  { title: 'Item Quantity', key: 'itemQty', align: 'left' },
  { title: 'Total Price', key: 'totalPrice', align: 'left' },
  { title: 'All Total', key: 'alltotalPrice', align: 'left' },
  { title: 'Vendor Bank Account', key: 'vendorBankAccount', align: 'left' },
  { title: 'Payment Status', key: 'paymentStatus', align: 'left' },
  { title: 'Payment Proof', key: 'paymentProof', align: 'left' },
  { title: 'Submission User', key: 'submissionUser', align: 'left' },
  { title: 'Submission Notes', key: 'submissionNotes', align: 'left' },
  { title: 'Verification Status', key: 'verificationStatus', align: 'left' },
  { title: 'Verification User', key: 'verificationUser', align: 'left' },
  { title: 'Verification Notes', key: 'verificationNotes', align: 'left' },
  { title: 'Actions', key: 'actions', align: 'left', sortable: false },
]);

// State untuk item yang akan dihapus
const editedIndex = ref(-1);
const editedItem = ref({});
const defaultItem = {
    id: '',
    orderDate: '',
    vendorData: '',
    itemName: '',
    itemDesc: '',
    itemPrice: '',
    itemQty: '',
    submitNotes: '',
};

// Fungsi untuk mengambil data dari API
const loadRequestPOs = async () => {
    try {
        const data = await fetchRequestPOs();
        productlist.value = data; // Simpan data dari API ke dalam state
    } catch (error) {
        console.error('Failed to load request POs:', error);
    }
};

// State untuk menyimpan data yang akan diubah
const editedPO = ref({
  poid: '',
  paymentProof: null,
  paymentStatus: '',
  verificationStatus: '',
  verificationNotes: '',
});

// Validasi agar tombol Update aktif jika salah satu input diisi
const validateUpdateFields = computed(() => {
  return (
    !!editedPO.value.paymentProof || // Periksa apakah paymentProof memiliki nilai
    !!editedPO.value.paymentStatus || // Periksa apakah paymentStatus memiliki nilai
    !!editedPO.value.verificationStatus || // Periksa apakah verificationStatus memiliki nilai
    !!editedPO.value.verificationNotes // Periksa apakah verificationNotes memiliki nilai
  );
});

const handleFileUpload = (event) => {
  const file = event.target.files[0]; // Ambil file pertama yang diunggah
  if (file) {
    editedPO.value.paymentProof = file.name; // Simpan nama file ke dalam state
  } else {
    editedPO.value.paymentProof = null; // Reset jika tidak ada file yang dipilih
  }
};

// Fungsi untuk membuka dialog Update
const openUpdateDialog = (item) => {
  editedPO.value = {
    poid: item.id,
    paymentProof: null, // Harus diisi dengan file jika ada
    paymentStatus: item.paymentStatus || '',
    verificationStatus: item.verificationStatus || '',
    verificationNotes: item.verificationNotes || '',
  };
  updateDialog.value = true;
};

// Fungsi untuk mengupdate PO
const updatePO = async () => {
  try {
    // Kirim data ke API
    await updateRequestPO(editedPO.value.poid, {
      paymentProof: editedPO.value.paymentProof,
      paymentStatus: editedPO.value.paymentStatus,
      verificationStatus: editedPO.value.verificationStatus,
      verificationNotes: editedPO.value.verificationNotes,
    });
    console.log('Request PO updated successfully');
    updateDialog.value = false;
    await loadRequestPOs(); // Refresh data tabel
  } catch (error) {
    console.error('Failed to update Request PO:', error);
  }
};

// Fungsi untuk menghapus item
const deleteItem = (item) => {
    editedIndex.value = productlist.value.indexOf(item);
    editedItem.value = { ...item };
    dialogDelete.value = true;
};

// Fungsi untuk mengonfirmasi penghapusan
const deleteItemConfirm = async () => {
    try {
        await deleteRequestPO(editedItem.value.id); // Hapus item melalui API
        productlist.value.splice(editedIndex.value, 1); // Hapus dari tabel
        dialogDelete.value = false;
    } catch (error) {
        console.error('Failed to delete item:', error);
    }
};

// Fungsi untuk menutup dialog delete
const closeDelete = () => {
    dialogDelete.value = false;
    Object.assign(editedItem.value, defaultItem);
    editedIndex.value = -1;
};

// Ambil data saat komponen dimuat
onMounted(() => {
    loadRequestPOs();
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
                    item-value="id"
                    color="primary"
                >
                    <!-- Kolom No -->
                    <template v-slot:item.no="{ index }">
                        <span class="text-subtitle-1 text-left">{{ index + 1 }}</span>
                    </template>
                    
                    <!-- Kolom lainnya -->
                    <template v-slot:item.id="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.id }}</span>
                    </template>
                    
                    <template v-slot:item.orderDate="{ item }">
                        <span class="text-subtitle-1 text-left">
                            {{ item.orderDate ? dayjs(item.orderDate).format('YYYY-MM-DD HH:mm:ss') : '-' }}
                            <!-- {{ item.orderDate }} -->
                        </span>
                    </template>

                    <template v-slot:item.vendorName="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.vendorName }}</span>
                    </template>

                    <template v-slot:item.vendorAddress="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.vendorAddress }}</span>
                    </template>

                    <template v-slot:item.vendorPhone="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.vendorPhone }}</span>
                    </template>

                    <!-- Kolom Item Name -->
                    <template v-slot:item.itemName="{ item }">
                        <ul>
                            <li v-for="name in item.itemName.split('|')" :key="name">{{ name }}</li>
                        </ul>
                    </template>

                    <!-- Kolom Item Description -->
                    <template v-slot:item.itemDesc="{ item }">
                        <ul>
                            <li v-for="desc in item.itemDesc.split('|')" :key="desc">{{ desc }}</li>
                        </ul>
                    </template>

                    <!-- Kolom Item Price -->
                    <template v-slot:item.itemPrice="{ item }">
                        <ul>
                            <li v-for="price in item.itemPrice.split('|')" :key="price">{{ price }}</li>
                        </ul>
                    </template>

                    <!-- Kolom Item Quantity -->
                    <template v-slot:item.itemQty="{ item }">
                        <ul>
                            <li v-for="qty in item.itemQty.split('|')" :key="qty">{{ qty }}</li>
                        </ul>
                    </template>

                    <template v-slot:item.totalPrice="{ item }">
                        <ul>
                            <li v-for="ttlprc in item.totalPrice.split('|')" :key="ttlprc">{{ ttlprc }}</li>
                        </ul>
                    </template>

                    <template v-slot:item.AllTotalPrice="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.AllTotalPrice }}</span>
                    </template>

                    <template v-slot:item.vendorBankAccount="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.vendorBankAccount }}</span>
                    </template>

                    <template v-slot:item.paymentStatus="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.paymentStatus }}</span>
                    </template>

                    <template v-slot:item.paymentProof="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.paymentProof }}</span>
                    </template>

                    <template v-slot:item.submissionUser="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.submissionUser }}</span>
                    </template>

                    <template v-slot:item.submissionNotes="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.submissionNotes }}</span>
                    </template>

                    <template v-slot:item.verificationStatus="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.verificationStatus }}</span>
                    </template>

                    <template v-slot:item.verificationUser="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.verificationUser }}</span>
                    </template>

                    <template v-slot:item.verificationNotes="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.verificationNotes }}</span>
                    </template>

                    <!-- Actions -->
                    <template v-slot:item.actions="{ item }">
                        <div class="d-flex gap-2 justify-left">
                            <EditIcon
                            height="20"
                            width="20"
                            class="text-primary cursor-pointer"
                            @click="openUpdateDialog(item)"
                            />
                            <TrashIcon
                            height="20"
                            width="20"
                            class="text-error cursor-pointer"
                            @click="deleteItem(item)"
                            />
                        </div>
                    </template>
                </v-data-table>
            </UiParentCard>
        </v-col>
    </v-row>

    <!-- Dialog Update -->
    <v-dialog v-model="updateDialog" max-width="500">
        <v-card>
            <v-card-title>Update Request PO</v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-select
                            v-model="editedPO.paymentStatus"
                            :items="['PAID', 'UNPAID']"
                            label="Select Payment Status"
                            variant="outlined"
                            color="primary"
                            />
                        </v-col>
                        <v-col cols="12">
                            <v-select
                            v-model="editedPO.verificationStatus"
                            :items="['ACCEPT', 'PENDING', 'REJECT']"
                            label="Select Verification Status"
                            variant="outlined"
                            color="primary"
                            />
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                            v-model="editedPO.verificationNotes"
                            label="Enter Verification Notes"
                            variant="outlined"
                            color="primary"
                            />
                        </v-col>
                        <v-col cols="12">
                            <v-file-input
                                label="Upload Payment Proof"
                                accept="image/*"
                                variant="outlined"
                                color="primary"
                                @change="handleFileUpload"
                            />
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-btn text @click="updateDialog = false">Cancel</v-btn>
                <v-btn
                    color="primary"
                    @click="updatePO"
                    :disabled="!validateUpdateFields"
                >
                Update
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

    <!-- Dialog untuk konfirmasi delete -->
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
</template>

<style scoped>
/* Tambahkan styling jika diperlukan */
</style>