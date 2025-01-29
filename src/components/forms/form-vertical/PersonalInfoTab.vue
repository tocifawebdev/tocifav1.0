<script setup lang="ts">
import { ref } from 'vue';
import { processExcelFile, insertData, downloadTemplate as downloadTemplateAPI } from '@/_mockApis/apps/uploaditem/indexItemManagement';

/* Dropdown State */
const select = ref('');
const categories = ref(['BARANG MASUK', 'BARANG KELUAR']);
// const isDropdownOpen = ref(false); // State untuk dropdown terbuka

/* Calendar Picker State */
const isCalendarOpen = ref(false); // State untuk Date Picker aktif
const selectedDate = ref(''); // Menyimpan tanggal yang dipilih

/* File Upload State */
const uploadedFileName = ref(''); // Menyimpan nama file yang diunggah
const uploadedFile = ref<File | null>(null); // Menyimpan file yang diunggah

/* Download Template */
const downloadTemplate = async () => {
  if (!select.value) {
    alert('Silakan pilih kategori terlebih dahulu.');
    return;
  }

  try {
    await downloadTemplateAPI(select.value); // Memanggil fungsi download template dari API
    alert('Template berhasil diunduh.');
  } catch (error) {
    console.error('Error downloading template:', error);
    alert('Gagal mengunduh template. Silakan coba lagi.');
  }
};

/* Handle File Upload */
const handleFileUpload = async (event: Event) => {
  const file = (event.target as HTMLInputElement)?.files?.[0];
  if (file) {
    uploadedFileName.value = file.name; // Perbarui nama file yang diunggah
    uploadedFile.value = file; // Simpan file untuk pengolahan selanjutnya
  }
};

/* Handle Submit */
const handleSubmit = async () => {
  if (!select.value) {
    alert('Silakan pilih kategori.');
    return;
  }
  if (!selectedDate.value) {
    alert('Silakan pilih tanggal.');
    return;
  }
  if (!uploadedFile.value) {
    alert('Silakan unggah file Excel.');
    return;
  }

  try {
    // Proses file Excel
    const { itemName, itemQty, notes } = await processExcelFile(uploadedFile.value);

    // Kirim data ke server
    await insertData(select.value, selectedDate.value, itemName, itemQty, notes);

    alert('Data berhasil dimasukkan ke tabel utama.');
  } catch (error) {
    console.error('Error submitting data:', error);
    alert('Gagal memasukkan data.');
  }
};
</script>

<template>
  <v-row>
    <!-- Select Category -->
    <v-col cols="12" md="6">
      <div class="mb-6">
        <v-label class="font-weight-medium mb-2">Select Category</v-label>
        <v-select
          v-model="select"
          :items="categories"
          single-line
          variant="outlined"
          hide-details
        ></v-select>
      </div>

      <!-- Periode -->
      <div class="mb-6">
        <v-label class="font-weight-medium mb-2">Periode</v-label>
        <v-text-field
          v-model="selectedDate"
          color="primary"
          variant="outlined"
          type="date"
          hide-details
          @focus="isCalendarOpen = true"
          @blur="isCalendarOpen = false"
        ></v-text-field>
      </div>

      <!-- Upload Excel -->
      <div
        class="mb-6"
        :style="{
          marginTop: isCalendarOpen ? '195px' : '20px', /* Turunkan jarak saat Date Picker aktif */
          transition: 'margin 0.2s ease',
        }"
      >
        <v-label class="font-weight-medium mb-2">Upload Excel</v-label>
        <div
          :style="{
            border: '1px dashed #ccc',
            padding: '10px 20px', /* Sesuaikan padding */
            textAlign: uploadedFileName ? 'left' : 'center', /* Posisi teks dinamis */
            height: '110px', /* Tinggi yang sama dengan box periode */
            display: 'flex',
            alignItems: 'center',
            justifyContent: uploadedFileName ? 'flex-start' : 'center', /* Atur posisi */
            cursor: 'pointer',
          }"
          @click="$refs.fileInput.click()"
        >
          <template v-if="uploadedFileName">
            <!-- Nama file yang terupload -->
            <p style="margin: 0; color: #4CAF50;">{{ uploadedFileName }}</p>
          </template>
          <template v-else>
            <!-- Default teks upload -->
            Drag file kesini atau klik untuk memilih
            <v-icon color="#4CAF50" size="48" style="margin-left: 8px;">mdi-file-excel</v-icon>
          </template>
        </div>
        <input
          ref="fileInput"
          type="file"
          accept=".xlsx, .xls"
          style="display: none;"
          @change="handleFileUpload"
        />
      </div>

      <!-- Download Template -->
      <div
        class="mb-6"
        :style="{
          marginTop: '60px',
        }"
      >
        Klik disini untuk mendownload 
        <span
          @click="downloadTemplate"
          style="color: blue; cursor: pointer; text-decoration: underline;"
        >
          template
        </span>
      </div>
    </v-col>

    <!-- Button Submit -->
    <v-col
      cols="12"
      :style="{
        marginTop: '-20px',
      }"
    >
      <v-btn color="primary" flat @click="handleSubmit">Upload</v-btn>
    </v-col>
  </v-row>
</template>
