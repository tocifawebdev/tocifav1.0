<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { fetchVendorData } from '@/_mockApis/apps/requestpo/indexSelectvendor';
import { fetchVendorItems } from '@/_mockApis/apps/requestpo/IndexSelectVendoritem';
import { fetchCurrentDateTime } from '@/_mockApis/apps/requestpo/indexDateTime';
import { addRequestPO } from '@/_mockApis/apps/requestpo/indexRequestpo';


// State untuk data form
const purchaseDate = ref('');
const vendors = ref<{ VendorData: string; Address: string; Phone: string }[]>([]);
const selectedVendor = ref<{ VendorData: string; Address: string; Phone: string } | null>(null);
const vendorItems = ref<{ VendorItemData: string; ItemName: string; Price: number; Unit: string }[]>([]);
const selectedVendorItem = ref<{ VendorItemData: string; ItemName: string; Price: number; Unit: string } | null>(null);
const vendorAddress = ref('');
const vendorPhone = ref('');
const items = ref<{ barang: string; harga: number; jumlah: number; deskripsi: string; type: string }[]>([]);
const dialog = ref(false);
const notification = ref('');

// Ambil current datetime saat komponen dimuat
const getCurrentDateTime = async () => {
  try {
    purchaseDate.value = await fetchCurrentDateTime();
  } catch (error) {
    console.error('Failed to fetch current date and time:', error);
  }
};

// Ambil vendor data saat komponen dimuat
const getVendors = async () => {
  try {
    vendors.value = await fetchVendorData();
  } catch (error) {
    console.error('Failed to fetch vendor data:', error);
  }
};

// Ambil barang vendor berdasarkan vendor yang dipilih
const getVendorItems = async (vendordata: string) => {
  try {
    vendorItems.value = await fetchVendorItems(vendordata); // Kirim parameter vendor
    console.log('Vendor Items:', vendorItems.value);
  } catch (error) {
    console.error('Failed to fetch vendor items:', error);
  }
};

// Submit data PO
const handleSubmit = async () => {
  const requestData = {
    orderDate: purchaseDate.value,
    vendorData: selectedVendor.value?.VendorData || '',
    itemName: items.value.map((item) => item.barang).join(', '),
    itemDesc: items.value.map((item) => item.deskripsi).join(', '),
    itemPrice: items.value.reduce((total, item) => total + (item.harga || 0), 0),
    itemQty: items.value.reduce((total, item) => total + (item.jumlah || 0), 0),
    paymentProof: null,
    submitNotes: 'Notes Example',
  };

  try {
    await addRequestPO(requestData);
    notification.value = 'Purchase Order submitted successfully!';
    items.value = [];
  } catch (error) {
    console.error('Failed to submit purchase order:', error);
    notification.value = 'Failed to submit purchase order.';
  } finally {
    dialog.value = false;
  }
};

// Watch Vendor yang Dipilih
watch(selectedVendor, (newVendor) => {
  vendorAddress.value = newVendor?.Address || '';
  vendorPhone.value = newVendor?.Phone || '';
  if (newVendor?.VendorData) {
    getVendorItems(newVendor.VendorData); // Kirim vendor yang dipilih ke backend
  } else {
    vendorItems.value = [];
  }
});


// Watch Barang yang Dipilih
watch(selectedVendorItem, (newItem) => {
  if (newItem) {
    items.value.push({
      barang: newItem.ItemName,
      harga: newItem.Price,
      jumlah: 1,
      deskripsi: '',
      type: newItem.Unit,
    });
  }
});

// OnMounted Hooks
onMounted(() => {
  getCurrentDateTime();
  getVendors();
});

// Fungsi untuk menambah input barang baru
const addItem = () => {
  items.value.push({
    barang: '',
    harga: 0,
    jumlah: 1,
    deskripsi: '',
    type: '',
  });
};



// Fungsi untuk menghapus input barang terakhir
const removeItem = () => {
  if (items.value.length > 0) {
    items.value.pop();
  }
};
</script>
<template>
  <v-row>
    <v-col cols="12" lg="12">
      <!-- Bagian form lainnya -->
      <v-row>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Purchase Date</v-label>
          <v-text-field :value="purchaseDate" variant="outlined" color="primary" readonly></v-text-field>
          <v-label class="mb-2 font-weight-medium">Vendor Address</v-label>
          <v-text-field :value="vendorAddress" variant="outlined" color="primary" readonly></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Vendor</v-label>
          <v-select
            v-model="selectedVendor"
            :items="vendors"
            item-title="VendorData"
            return-object
            variant="outlined"
            color="primary"
            label="Select Vendor"
          ></v-select>
          <v-label class="mb-2 font-weight-medium">Vendor Phone</v-label>
          <v-text-field :value="vendorPhone" variant="outlined" color="primary" readonly></v-text-field>
        </v-col>
      </v-row>

      <!-- Tombol Tambah dan Hapus Barang -->
      <v-row>
        <v-col cols="12" class="d-flex align-center">
          <v-btn icon color="red" @click="addItem" class="mb-3">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-btn icon color="red" @click="removeItem" class="mb-3">
            <v-icon>mdi-minus</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <!-- Input Dinamis untuk Barang -->
      <v-row v-for="(item, index) in items" :key="index" class="mb-3">
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Item</v-label>
          <v-select
  v-model="selectedVendorItem"
  :items="vendorItems"
  item-title="VendorItemData"
  return-object
  variant="outlined"
  color="primary"
  label="Select Item"
></v-select>

          <v-label class="mb-2 font-weight-medium">Item Price</v-label>
          <v-text-field v-model="item.harga" variant="outlined" color="primary" readonly></v-text-field>
          <v-label class="mb-2 font-weight-medium">Total Per Item Price</v-label>
          <v-text-field
            :value="item.harga * item.jumlah"
            variant="outlined"
            color="primary"
            readonly
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Item Type</v-label>
          <v-text-field v-model="item.type" variant="outlined" color="primary" readonly></v-text-field>
          <v-label class="mb-2 font-weight-medium">Total Items</v-label>
          <v-text-field v-model="item.jumlah" type="number" variant="outlined" color="primary"></v-text-field>
          <v-label class="mb-2 font-weight-medium">Item Description</v-label>
          <v-text-field v-model="item.deskripsi" variant="outlined" color="primary"></v-text-field>
        </v-col>
      </v-row>

      <!-- Total Harga Semua Item -->
      <v-row>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Total All Item Price</v-label>
          <v-text-field
            :value="items.reduce((total, item) => total + item.harga * item.jumlah, 0)"
            variant="outlined"
            color="primary"
            readonly
          ></v-text-field>
        </v-col>
      </v-row>

      <!-- Tombol Submit -->
      <v-row>
        <v-col cols="12">
          <v-btn color="primary" @click="dialog = true">Submit</v-btn>
          <v-alert v-if="notification" type="success" class="mt-3">{{ notification }}</v-alert>
        </v-col>
      </v-row>

      <!-- Dialog Pop-up -->
      <v-dialog v-model="dialog" max-width="500">
        <v-card>
          <v-card-title>Confirmation</v-card-title>
          <v-card-text>Are you sure you want to submit this Purchase Order?</v-card-text>
          <v-card-actions>
            <v-btn text @click="dialog = false">Cancel</v-btn>
            <v-btn color="primary" @click="handleSubmit">Confirm</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-col>
  </v-row>
</template>
