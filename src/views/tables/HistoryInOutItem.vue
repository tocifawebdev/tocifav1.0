<script setup>
import { ref, onMounted } from 'vue';
import { EditIcon, TrashIcon } from 'vue-tabler-icons';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import axios from 'axios';

const search = ref('');
const productlist = ref([]);
const select = ref(null); 
const selectedDate = ref(null); 
const categories = ref(['BARANG MASUK', 'BARANG KELUAR']);
const showTable = ref(false);

const API_BASE_URL = 'http://127.0.0.1:8000/itemmanagement/';

async function fetchData(category, date) {
    try {
        const response = await axios.get(API_BASE_URL, {
            params: {
                category,
                date,
            },
        });
        const rawData = response.data[category] || [];
    
        // Filter data berdasarkan periode (tanggal)
        const filteredData = rawData.filter((item) => {
            const itemDate = item.DateInOut ? item.DateInOut.split('T')[0] : null; 
            return itemDate === date; 
        });

        productlist.value = filteredData.map((item) => ({
            name: item.ItemName,
            quantity: item.ItemQty,
            notes: item.Notes,
            periode: date, 
            createUser: item.AddUser || '01700551', 
        }));
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('Gagal mengambil data.');
    }
}

function handleShow() {
    if (select.value && selectedDate.value) {
        fetchData(select.value, selectedDate.value);
        showTable.value = true;
    } else {
        alert('Please select both category and period.');
    }
}

onMounted(() => {
    productlist.value = [];
});
</script>

<template>
    <v-row>
        <v-col cols="12">
            <UiParentCard title="History Items In-Out">
                <!-- Elemen untuk memilih kategori dan periode -->
                <v-row class="mb-4">
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
                                style="max-width: 300px;"
                            ></v-select>
                        </div>
                    </v-col>
                </v-row>
                <v-row class="mb-4">
                    <!-- Periode -->
                    <v-col cols="12" md="6"
                    :style="{
                    marginTop: '-30px',
                    }">
                        <div class="mb-6">
                            <v-label class="font-weight-medium mb-2">Periode</v-label>
                            <v-text-field
                                color="primary"
                                variant="outlined"
                                type="date"
                                hide-details
                                v-model="selectedDate"
                                style="max-width: 300px;"
                            ></v-text-field>
                        </div>
                    </v-col>
                </v-row>
                <v-row class="mb-4">
                    <!-- Tombol Show -->
                    <v-col cols="12"
                    :style="{
                    marginTop: '-30px',
                    marginBottom: '20px',
                    }">
                        <v-btn color="primary" flat @click="handleShow">Show</v-btn>
                    </v-col>
                </v-row>
                <!-- Search bar muncul hanya jika tabel ditampilkan -->
                <v-row v-if="showTable" class="mb-4">
                    <v-col cols="12" class="d-flex justify-end">
                        <v-text-field
                            v-model="search"
                            append-inner-icon="mdi-magnify"
                            label="Search"
                            single-line
                            hide-details
                            class="mb-md-0 mb-4"
                            style="max-width: 270px;"
                        />
                    </v-col>
                </v-row>
                <!-- Tabel hanya muncul jika showTable bernilai true -->
                <v-data-table
                    v-if="showTable"
                    class="rounded-md datatabels productlist"
                    :headers="headers"
                    :items="productlist"
                    v-model:search="search"
                    items-per-page="5"
                    item-value="name"
                    color="primary"
                >
                    <!-- Kolom Item Name -->
                    <template v-slot:item.name="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.name }}</span>
                    </template>

                    <!-- Kolom Item Quantity -->
                    <template v-slot:item.quantity="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.quantity }}</span>
                    </template>

                    <!-- Kolom Notes -->
                    <template v-slot:item.notes="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.notes }}</span>
                    </template>

                    <!-- Kolom Periode -->
                    <template v-slot:item.periode="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.periode }}</span>
                    </template>

                    <!-- Kolom Create User -->
                    <template v-slot:item.createUser="{ item }">
                        <span class="text-subtitle-1 text-left">{{ item.createUser }}</span>
                    </template>

                    <!-- Slot untuk ketika tidak ada data -->
                    <template v-slot:no-data>
                        <v-btn color="primary" @click="initialize">Reset</v-btn>
                    </template>
                </v-data-table>
            </UiParentCard>
        </v-col>
    </v-row>
</template>
