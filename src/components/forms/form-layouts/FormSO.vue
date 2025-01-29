<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { fetchCurrentDateTime } from '@/_mockApis/apps/requestso/indexDateTime';
import { fetchCustomerData } from '@/_mockApis/apps/requestso/indexSelectCustomer';
import { fetchCustomerItems } from '@/_mockApis/apps/requestso/indexSelectCustomerItem';
import { addRequestSO } from '@/_mockApis/apps/requestso/indexRequestSo';

// State untuk data form
const purchaseDate = ref('');
const customers = ref<{ CustomerData: string; Address: string; Phone: string; BankAccount: string }[]>([]);
const selectedCustomer = ref<{ CustomerData: string; Address: string; Phone: string; BankAccount: string } | null>(null);
const customerItems = ref<{ CustomerItemData: string; ItemName: string; Unit: string }[]>([]);
const items = ref<
  { barang: string | { CustomerItemData: string; ItemName: string; Unit: string }; price: number; jumlah: number; deskripsi: string; type: string }[]
>([]);
const notification = ref('');
const paymentMethod = ref('');
const additionalPrice = ref<number>(0); // Ensure this is a number
const tax = ref<number>(0);
const dialog = ref(false);
const editedItem = ref({ verificationStatus: '', paymentStatus: '' });

// Computed properties
const subtotal = computed((): string =>
  items.value
    .reduce((total, item) => total + item.price * item.jumlah, 0)
    .toFixed(2) // Pastikan hasil memiliki dua angka desimal
);

// const totalBeforeTax = computed((): string => {
//   // Pastikan nilai ref diakses dengan .value
//   const subtotalValue: number = parseFloat(subtotal.value || '0'); // Konversi ke number
//   const additionalValue: number = parseFloat(additionalPrice.value || '0'); // Konversi ke number

//   // Tambahkan kedua nilai
//   const total: number = subtotalValue + additionalValue;

//   // Kembalikan sebagai string dengan 2 angka desimal
//   return total.toFixed(2);
// });

// Total sebelum pajak (string pada akhirnya)
const totalBeforeTax = computed((): string => {
  const subtotalValue: number = parseFloat(`${subtotal.value || '0'}`); // Paksa ke string
  const additionalValue: number = parseFloat(`${additionalPrice.value || '0'}`); // Paksa ke string
  const total: number = subtotalValue + additionalValue; // Perhitungan dalam bentuk decimal
  return total.toFixed(2); // Kembalikan hasil sebagai string dengan 2 angka desimal
});

watch(tax, (newTax) => {
  if (newTax < 0) {
    tax.value = 0; // Tidak boleh negatif
  }
});

// const tax = computed(() => tax.value);

// Total setelah pajak (string pada akhirnya)
const totalAfterTax = computed((): string => {
  const totalBefore: number = parseFloat(totalBeforeTax.value || '0'); // Konversi string ke angka
  const taxValue: number = parseFloat(tax.value?.toString() || '0') / 100; // Ubah PPN menjadi persentase (5% => 0.05)
  const totalWithTax: number = totalBefore + totalBefore * taxValue; // Perhitungan total dengan pajak
  return totalWithTax.toFixed(2); // Kembalikan hasil sebagai string dengan 2 desimal
});

// Fetch current datetime
const getCurrentDateTime = async () => {
  try {
    purchaseDate.value = await fetchCurrentDateTime();
  } catch (error) {
    console.error('Failed to fetch current date and time:', error);
  }
};

// Fetch customer data
const getCustomers = async () => {
  try {
    customers.value = await fetchCustomerData();
  } catch (error) {
    console.error('Failed to fetch customer data:', error);
  }
};

// Fetch customer items
const getCustomerItems = async () => {
  try {
    customerItems.value = await fetchCustomerItems();
  } catch (error) {
    console.error('Failed to fetch customer items:', error);
  }
};

// Watch selected customer for automatic updates
watch(selectedCustomer, (newCustomer) => {
  if (newCustomer) {
    paymentMethod.value = newCustomer.BankAccount || '';
  }
});

// Watch items for automatic updates
watch(
  items,
  (newItems) => {
    newItems.forEach((item, index) => {
      if (typeof item.barang === 'object') {
        const selectedItem = item.barang as { CustomerItemData: string; ItemName: string; Unit: string; Price: number };
        items.value[index].type = selectedItem.Unit || '';
      }
    });
  },
  { deep: true }
);

// Add new item
const addItem = () => {
  items.value.push({ barang: '', price: 0, jumlah: 1, deskripsi: '', type: '' });
};

// Remove last item
const removeItem = () => {
  if (items.value.length > 0) {
    items.value.pop();
  }
};

// Submit form
const submitForm = async () => {
  // Validasi data sebelum submit
  if (!purchaseDate.value || !selectedCustomer.value || !items.value.length) {
    notification.value = 'All fields are required!';
    return;
  }

  // Data untuk dikirim
  const requestData = {
    orderdate: purchaseDate.value,
    customerdata: selectedCustomer.value?.CustomerData || '',
    itemname: items.value.map(item => (typeof item.barang === 'object' ? item.barang.ItemName : item.barang)).join('|'),
    itemdesc: items.value.map(item => item.deskripsi).join('|'),
    itemprice: items.value.map(item => item.price).join('|'),
    itemunit: items.value.map(item => item.type).join('|'),
    itemqty: items.value.map(item => item.jumlah).join('|'),
    itemaddprice: additionalPrice.value,
    ppn: tax.value,
    submitnotes: editedItem.value.paymentStatus || 'Notes Example',
  };

  try {
    await addRequestSO(requestData);
    notification.value = 'Request SO submitted successfully!';
    dialog.value = false; // Tutup dialog setelah submit
  } catch (error) {
    console.error('Failed to submit requestso data:', error);
    notification.value = 'Failed to submit requestso data.';
  }
};

// OnMounted hooks
onMounted(() => {
  getCurrentDateTime();
  getCustomers();
  getCustomerItems();
});
</script>

<template>
  <v-row>
    <v-col cols="12" lg="12">
      <!-- Form Header -->
      <v-row>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Purchase Date</v-label>
          <v-text-field :value="purchaseDate" variant="outlined" color="primary" readonly></v-text-field>
          <v-label class="mb-2 font-weight-medium">Customer Address</v-label>
          <v-text-field :value="selectedCustomer?.Address" variant="outlined" color="primary" readonly></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Customer Name</v-label>
          <v-select
            v-model="selectedCustomer"
            :items="customers"
            item-title="CustomerData"
            return-object
            variant="outlined"
            color="primary"
          ></v-select>
          <v-label class="mb-2 font-weight-medium">Customer Phone Number</v-label>
          <v-text-field :value="selectedCustomer?.Phone" variant="outlined" color="primary" readonly></v-text-field>
        </v-col>
      </v-row>

      <!-- Add/Remove Items -->
      <v-row>
        <v-col cols="12" class="d-flex align-center">
          <v-btn color="success" @click="addItem" outlined rounded>
            <v-icon left>mdi-plus</v-icon> Add Item
          </v-btn>
          <v-btn color="error" class="ml-3" @click="removeItem" outlined rounded>
            <v-icon left>mdi-minus</v-icon> Remove Item
          </v-btn>
        </v-col>
      </v-row>

      <!-- Item Input -->
      <v-row v-for="(item, index) in items" :key="index" class="mb-3">
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Item</v-label>
          <v-select
            v-model="items[index].barang"
            :items="customerItems"
            item-title="CustomerItemData"
            return-object
            variant="outlined"
            color="primary"
          ></v-select>
          <v-label class="mb-2 font-weight-medium">Item Price</v-label>
          <v-text-field v-model="item.price" type="number" placeholder="Masukkan Harga Barang (Rp)" variant="outlined" color="primary"></v-text-field>
          <v-label class="mb-2 font-weight-medium">Total Per Item Price</v-label>
          <v-text-field
            :value="item.jumlah * item.price"
            variant="outlined"
            color="primary"
            readonly
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Item Type</v-label>
          <v-text-field v-model="item.type" variant="outlined" color="primary" readonly></v-text-field>
          <v-label class="mb-2 font-weight-medium">Total Items</v-label>
          <v-text-field v-model="item.jumlah" type="number" placeholder="Masukkan Jumlah Barang" variant="outlined" color="primary"></v-text-field>
          <v-label class="mb-2 font-weight-medium">Item Description</v-label>
          <v-text-field v-model="item.deskripsi" placeholder="Masukkan Deskripsi Barang (Jika Ada)" variant="outlined" color="primary"></v-text-field>
        </v-col>
      </v-row>

      <!-- Calculations -->
      <v-row>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Sub Total All Item Price</v-label>
          <v-text-field :value="subtotal" variant="outlined" color="primary" readonly></v-text-field>
          <v-label class="mb-2 font-weight-medium">Total All Item Price (Before Tax)</v-label>
          <v-text-field :value="totalBeforeTax" variant="outlined" color="primary" readonly></v-text-field>
          <v-label class="mb-2 font-weight-medium">Total All Item Price (After Tax)</v-label>
          <v-text-field :value="totalAfterTax" variant="outlined" color="primary" readonly></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Additional Price (Rp)</v-label>
          <v-text-field v-model="additionalPrice" type="number" placeholder="Masukkan Biaya Tambahan (Rp) (Jika Ada)" variant="outlined" color="primary"></v-text-field>
          <v-label class="mb-2 font-weight-medium">PPN (%)</v-label>
          <v-text-field v-model="tax" type="number" step="0.01" placeholder="Masukkan PPN (%)" variant="outlined" color="primary"></v-text-field>
        </v-col>
      </v-row>

      <!-- Submit -->
      <v-row>
        <v-col cols="12">
          <v-btn color="primary" class="mt-3" @click="dialog = true">Submit</v-btn>
          <v-alert v-if="notification" type="success" class="mt-3">{{ notification }}</v-alert>
        </v-col>

        <!-- Dialog Pop-up -->
        <v-dialog v-model="dialog" max-width="600">
          <v-card>
            <v-card-title>Confirmation</v-card-title>
            <v-card-text>
              <v-container class="px-0">
                <v-row>
                  <!-- Admin ID -->
                  <v-col cols="12">
                    <v-label class="mb-2 font-weight-medium">Admin ID</v-label>
                    <div class="text font-weight-medium" style="font-size: 14px;">01700551</div>
                  </v-col>
                  <!-- SO Description -->
                  <v-col cols="12">
                    <v-label class="mb-2 font-weight-medium">SO Description</v-label>
                    <v-text-field
                      v-model="editedItem.paymentStatus"
                      label=""
                      placeholder="Enter SO Description"
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
    </v-col>
  </v-row>
</template>
