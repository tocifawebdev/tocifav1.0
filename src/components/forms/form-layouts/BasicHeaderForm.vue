<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { fetchVendorData } from '@/_mockApis/apps/requestpo/indexSelectVendor';
import { fetchVendorItems } from '@/_mockApis/apps/requestpo/indexSelectVendorItem';
import { fetchCurrentDateTime } from '@/_mockApis/apps/requestpo/indexDateTime';
import { addRequestPO } from '@/_mockApis/apps/requestpo/indexRequestPo';

const purchaseDate = ref('');
const vendors = ref<{ VendorData: string; Address: string; Phone: string }[]>([]);
const selectedVendor = ref<{ VendorData: string; Address: string; Phone: string; BankAccount: string } | null>(null);
const vendorItems = ref<{ VendorItemData: string; ItemName: string; Price: number; Unit: string }[]>([]);
// const selectedVendorItem = ref<{ VendorItemData: string; ItemName: string; Price: number; Unit: string } | null>(null);
const vendorAddress = ref('');
const vendorPhone = ref('');
const items = ref<
  { barang: string | { VendorItemData: string; ItemName: string; Price: number; Unit: string }; harga: number; jumlah: number; deskripsi: string; type: string }[]
>([]);
const dialog = ref(false);
const notification = ref('');
const paymentMethod = ref('');
const adminId = ref('91790331');
const editedItem = ref({ verificationStatus: '', paymentStatus: '' });

// Get current datetime 
const getCurrentDateTime = async () => {
  try {
    purchaseDate.value = await fetchCurrentDateTime();
  } catch (error) {
    console.error('Failed to fetch current date and time:', error);
  }
};

// Get vendor data 
const getVendors = async () => {
  try {
    vendors.value = await fetchVendorData();
  } catch (error) {
    console.error('Failed to fetch vendor data:', error);
  }
};

// Get barang vendor 
const getVendorItems = async (vendordata: string) => {
  if (!vendordata) {
    vendorItems.value = [];
    return;
  }

  try {
    vendorItems.value = await fetchVendorItems(vendordata);
  } catch (error) {
    console.error('Failed to fetch vendor items:', error);
    vendorItems.value = [];
  }
};

// Watch Vendor yang Dipilih
watch(selectedVendor, (newVendor) => {
  vendorAddress.value = newVendor?.Address || '';
  vendorPhone.value = newVendor?.Phone || '';
  paymentMethod.value = newVendor?.BankAccount || '';

  if (newVendor?.VendorData) {
    getVendorItems(newVendor.VendorData);
  } else {
    vendorItems.value = [];
  }
});

// Watch Barang yang Dipilih
watch(
  items,
  (newItems) => {
    newItems.forEach((item, index) => {
      if (typeof item.barang === 'object') {
        // Pastikan barang adalah objek
        items.value[index].harga = item.barang.Price || 0;
        items.value[index].type = item.barang.Unit || '';
        items.value[index].barang = `${item.barang.VendorItemData}`;
      }
    });
  },
  { deep: true } // Perlu deep untuk mendeteksi perubahan dalam array
);

// Fungsi untuk menambah input barang baru
const addItem = () => {
  items.value.push({
    barang: '', // Nama barang awal kosong
    harga: 0,
    jumlah: 1,
    deskripsi: '',
    type: '',
  });
};

// Fungsi untuk menghapus input barang terakhir
const removeItem = () => {
  if (items.value.length > 0) {
    items.value.pop(); // Hapus elemen terakhir
  }
};

// Fungsi untuk submit form
const submitForm = async () => {
  if (!purchaseDate.value) {
    notification.value = 'Purchase date is required!';
    console.error('Purchase date is missing');
    return;
  }

  if (!selectedVendor.value) {
    notification.value = 'Vendor selection is required!';
    console.error('Vendor is not selected');
    return;
  }

  if (!items.value.length) {
    notification.value = 'At least one item is required!';
    console.error('Items are missing');
    return;
  }

  const validItems = items.value.map((item) => ({
    ...item,
    deskripsi: item.deskripsi || '',
  }));

  const requestData = {
    orderdate: purchaseDate.value,
    vendordata: selectedVendor.value?.VendorData || '',
    itemname: validItems.map((item) => item.barang).join('|'),
    itemdesc: validItems.map((item) => item.deskripsi).join('|'),
    itemprice: validItems.map((item) => item.harga).join('|'),
    itemunit: validItems.map((item) => item.type).join('|'),
    itemqty: validItems.map((item) => item.jumlah).join('|'),
    paymentproof: null,
    submitnotes: editedItem.value.paymentStatus || 'Notes Example',
  };

  try {
    const response = await addRequestPO(requestData);
    console.log('API response:', response);
    notification.value = 'Purchase Order submitted successfully!';
    items.value = [];
  } catch (error) {
    console.error('Failed to submit purchase order:', error);
    notification.value = 'Failed to submit purchase order.';
  } finally {
    dialog.value = false;
  }
};

// OnMounted Hooks
onMounted(() => {
  getCurrentDateTime();
  getVendors();
});
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
          <!-- Tombol Add Item -->
          <v-btn
            class="d-flex align-center"
            elevation="2"
            @click="addItem"
            style="background-color: transparent; border: none; padding: 0;"
          >
            <!-- Ikon dengan background abu-abu -->
            <div
              class="icon-bg"
              style="background-color: #808080; height: 20px; width: 20px; display: flex; align-items: center; justify-content: center;"
            >
              <v-icon>mdi-plus</v-icon>
            </div>
            <!-- Tulisan dengan background biru -->
            <div
              class="text-bg"
              style="background-color: #0000ff; color: white; flex: 1; height: 20px; width: 80px; display: flex; align-items: center; justify-content: center; font-weight: bold; text-transform: uppercase;"
            >
              Add Item
            </div>
          </v-btn>

          <!-- Tombol Remove Item -->
          <v-btn
            class="d-flex align-center"
            elevation="2"
            @click="removeItem"
            style="background-color: transparent; border: none; padding: 0; margin-left: 10px;"
          >
            <!-- Ikon dengan background abu-abu -->
            <div
              class="icon-bg"
              style="background-color: #808080; height: 20px; width: 20px; display: flex; align-items: center; justify-content: center;"
            >
              <v-icon>mdi-minus</v-icon>
            </div>
            <!-- Tulisan dengan background merah -->
            <div
              class="text-bg"
              style="background-color: #ff0000; color: white; flex: 1; height: 20px; width: 110px; display: flex; align-items: center; justify-content: center; font-weight: bold; text-transform: uppercase;"
            >
              Remove Item
            </div>
          </v-btn>
        </v-col>
      </v-row>

      <!-- Input Dinamis untuk Barang -->
      <v-row v-for="(item, index) in items" :key="index" class="mb-3">
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Item</v-label>
          <v-select
            v-model="items[index].barang"
            :items="vendorItems"
            item-title="VendorItemData"
            return-object
            variant="outlined"
            color="primary"
            label="Select Item"
          />
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
          <v-label class="mb-2 font-weight-medium">Payment Recipe</v-label>
          <v-file-input
            accept="image/*"
            label="File input"
            hide-details
            variant="outlined"
          ></v-file-input>   
        </v-col>                  
      <!-- Bagian Payment Recipe, Payment Method, Admin Id -->                       
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Payment Method</v-label>
          <v-text-field v-model="paymentMethod" variant="outlined" color="primary" readonly></v-text-field>
          <v-label class="mb-2 font-weight-medium">Admin Id</v-label>
          <v-text-field v-model="adminId" variant="outlined" color="primary" readonly></v-text-field>
        </v-col>
      </v-row>

      <!-- Tombol Submit -->
      <v-row>
        <v-col cols="12">
          <v-btn color="primary" class="mt-3" @click="dialog = true">Submit</v-btn>
          <v-alert v-if="notification" type="success" class="mt-3">{{ notification }}</v-alert>
        </v-col>
      </v-row>
    </v-col>

      <!-- Dialog Pop-up -->
      <v-dialog v-model="dialog" max-width="600">
        <v-card>
          <v-card-title>Confirmation</v-card-title>
          <v-card-text>
            <v-container class="px-0">
              <v-row>
                <!-- Admin ID sebagai teks statis -->
                <v-col cols="12">
                  <v-label class="mb-2 font-weight-medium">Admin ID</v-label>
                  <div class="text font-weight-medium" style="font-size: 14px;">01700551</div>
                </v-col>
                <!-- PO Description dengan box lebih lebar -->
                <v-col cols="12">
                  <v-label class="mb-2 font-weight-medium">PO Description</v-label>
                  <v-text-field
                    v-model="editedItem.paymentStatus"
                    label=""
                    placeholder="Enter PO Description"
                    variant="outlined"
                    color="primary"
                    style="height: 150%;" 
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-btn variant="text" @click="dialog = false">Cancel</v-btn>
            <v-btn color="primary" @click="submitForm">Confirm</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-row>
</template>

<style scoped>
.add-item-btn, .remove-item-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-radius: 5px;
  min-width: 50px;
  height: 50px;
  margin-right: 10px;
  overflow: hidden;
}

.icon-bg {
  background-color: #808080; /* Background abu-abu */
  height: 100%;
  width: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.text-bg {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  height: 100%;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 14px;
  color: white;
}

.blue-text {
  background-color: #024d1c; /* Background biru */
}

.red-text {
  background-color: #9ca70a; /* Background merah */
}

.add-item-btn:hover .blue-text, .remove-item-btn:hover .red-text {
  opacity: 0.8;
}

.add-item-btn:hover .icon-bg, .remove-item-btn:hover .icon-bg {
  opacity: 0.8;
}
</style>