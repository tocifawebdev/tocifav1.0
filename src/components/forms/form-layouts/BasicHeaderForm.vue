<script setup lang="ts">
import { ref } from 'vue';

// State untuk data form
const gender = ref(['Male', 'Female']);
const items = ref([]); // Menyimpan input dinamis untuk barang
const dialog = ref(false); // State untuk menampilkan dialog

// Fungsi untuk menambah input barang baru
const addItem = () => {
  items.value.push({
    barang: '',
    harga: '',
    jumlah: '',
    deskripsi: ''
  });
};

// Data untuk input di dalam dialog
const editedItem = ref({
  paymentStatus: '',
  verificationStatus: '',
  recipeStatusFile: null,
});

// Fungsi untuk menghapus input barang berdasarkan indeks
const removeItem = (index: number) => {
  items.value.splice(index, 1);
};

// Fungsi untuk membuka dialog saat Submit diklik
const handleSubmit = () => {
  dialog.value = true;
};
</script>

<template>
  <v-row>
    <v-col cols="12" lg="12">
      <!-- Bagian form lainnya -->
      <v-row>
        <v-col cols="12" md="6">
                    <v-label class="mb-2 font-weight-medium">Vendor</v-label>
                    <v-select :items="gender" item-title="gender" item-value="abbr" return-object single-line variant="outlined"></v-select>
                    <v-label class="mb-2 font-weight-medium">Vendor Address</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Purchase Date</v-label>
                    <v-text-field color="primary" variant="outlined" type="date" ></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Vendor Phone Number</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Item</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Item Price</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Total Items</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                    <v-label class="mb-2 font-weight-medium">Item Type</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Item Description</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Total Per Item Price</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Total Items Price</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Payment Method</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    
                    <v-label class="mb-2 font-weight-medium">Admin Id</v-label>
                    <v-text-field variant="outlined" color="primary"></v-text-field>
                    <v-label class="mb-2 font-weight-medium">Payment Recipe</v-label>
                    <v-file-input
                    accept="image/*"
                    label="File input" 
                    hide-details
                    variant="outlined"
                    ></v-file-input>
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
          <v-text-field variant="outlined" color="primary" v-model="item.barang"></v-text-field>
          <v-label class="mb-2 font-weight-medium">Item Price</v-label>
          <v-text-field variant="outlined" color="primary" v-model="item.harga"></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-label class="mb-2 font-weight-medium">Total Items</v-label>
          <v-text-field variant="outlined" color="primary" v-model="item.jumlah"></v-text-field>
          <v-label class="mb-2 font-weight-medium">Item Description</v-label>
          <v-text-field variant="outlined" color="primary" v-model="item.deskripsi"></v-text-field>
          <!-- Tombol Hapus Barang -->
        </v-col>
      </v-row>

      <!-- Tombol Submit -->
      <v-row>
        <v-col cols="12">
            <v-btn color="primary" class="mt-3" @click="handleSubmit">
            Submit
            </v-btn>
        </v-col>
      </v-row>
    </v-col>
    <!-- Dialog Pop-up -->
    <v-dialog v-model="dialog" max-width="500">
            <v-card>
                <v-card-title>Confirmation</v-card-title>
                <v-card-text>
                <v-container class="px-0">
                    <v-row>
                    <!-- Payment Status sebagai Input Text -->
                    <v-col cols="12">
                        <v-label class="mb-2 font-weight-medium">PO Description</v-label>
                        <v-text-field
                        v-model="editedItem.paymentStatus"
                        label=""
                        placeholder="Enter Payment Status"
                        variant="outlined"
                        color="primary"
                        ></v-text-field>
                    </v-col>

                    <!-- Verification Status sebagai teks terkunci -->
                    <v-col cols="12">
                        <v-label class="mb-2 font-weight-medium">Admin ID</v-label>
                        <v-text-field
                        v-model="editedItem.verificationStatus"
                        label=""
                        readonly
                        variant="outlined"
                        color="primary"
                        ></v-text-field>
                    </v-col>
                    </v-row>
                </v-container>
                </v-card-text>

                <v-card-actions>
                    <v-btn text @click="dialog = false">Cancel</v-btn>
                    <v-btn color="primary" @click="dialog = false">Confirm</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
  </v-row>
</template>
