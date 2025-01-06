<script setup>
import { ref, computed, onMounted } from 'vue';
import { EditIcon, TrashIcon } from 'vue-tabler-icons';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import {
  fetchVendorItems,
  addVendorItem,
  updateVendorItem,
  deleteVendorItem,
} from '@/_mockApis/apps/supplymanagement/indexVendorItem';
import { fetchDropdownVendors } from '@/_mockApis/apps/supplymanagement/indexListVendor';

const search = ref('');
const dialog = ref(false);
const dialogDelete = ref(false);
const dropdownVendors = ref([]);
const headers = ref([
  { title: 'No', key: 'no', align: 'left' },
  { title: 'ID', key: 'id', align: 'left' },
  { title: 'Vendor Name', key: 'status', align: 'left' }, // status -> VendorName
  { title: 'Item Name', key: 'product', align: 'left' }, // product -> ItemName
  { title: 'Price', key: 'price', align: 'left' },
  { title: 'Unit', key: 'rekening', align: 'left', sortable: false }, // rekening -> Unit
  { title: 'Actions', key: 'actions', align: 'left', sortable: false },
]);

const productlist = ref([]);
const editedIndex = ref(-1);
const editedItem = ref({
  id: '',
  status: '',
  product: '',
  price: '',
  rekening: '',
});
const defaultItem = {
  id: '',
  status: '',
  product: '',
  price: '',
  rekening: '',
};

const formTitle = computed(() => (editedIndex.value === -1 ? 'New Vendor Item' : 'Edit Vendor Item'));

async function initialize() {
  try {
    productlist.value = await fetchVendorItems();
    dropdownVendors.value = await fetchDropdownVendors();
  } catch (error) {
    console.error('Failed to initialize data:', error);
  }
}

function editItem(item) {
  editedIndex.value = productlist.value.indexOf(item);
  editedItem.value = { ...item };
  dialog.value = true;
}

function deleteItem(item) {
  editedIndex.value = productlist.value.indexOf(item);
  editedItem.value = { ...item };
  dialogDelete.value = true;
}

async function deleteItemConfirm() {
  try {
    if (!editedItem.value.id) {
      console.error('Item ID is missing');
      return;
    }

    // Panggil API untuk menghapus data
    await deleteVendorItem(editedItem.value.id);

    // Refresh data setelah penghapusan berhasil
    await initialize();

    // Tutup dialog delete
    closeDelete();
  } catch (error) {
    console.error('Failed to delete vendor item:', error);
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
      await updateVendorItem(editedItem.value);
      Object.assign(productlist.value[editedIndex.value], editedItem.value);
    } else {
      const newVendorItem = { ...editedItem.value };
      delete newVendorItem.id;
      await addVendorItem(newVendorItem);
      await initialize();
    }
    close();
  } catch (error) {
    console.error('Failed to save vendor item:', error);
  }
}

onMounted(initialize);
</script>

<template>
  <v-row>
    <v-col cols="12">
      <UiParentCard title="Vendor Items">
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
          <!-- Kolom Vendor Name -->
          <template v-slot:item.status="{ item }">
            <span class="text-subtitle-1 text-left">{{ item.status }}</span>
          </template>
          <!-- Kolom Item Name -->
          <template v-slot:item.product="{ item }">
            <span class="text-subtitle-1 text-left">{{ item.product }}</span>
          </template>
          <!-- Kolom Price -->
          <template v-slot:item.price="{ item }">
            <span class="text-subtitle-1 text-left">{{ item.price }}</span>
          </template>
          <!-- Kolom Unit -->
          <template v-slot:item.rekening="{ item }">
            <span class="text-subtitle-1 text-left">{{ item.rekening || '-' }}</span>
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
                    <v-btn color="primary" variant="flat" dark v-bind="props">Add New Item</v-btn>
                  </div>
                </template>
                <v-card>
                  <v-card-title class="pa-4 bg-primary">
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>
                  <v-card-text>
                    <v-container class="px-0">
                      <v-row>
                        <v-col cols="12">
                          <v-select
                            v-model="editedItem.status"
                            label="Vendor Name"
                            :items="dropdownVendors.map((vendor) => vendor.VendorData)"
                            outlined
                          ></v-select>
                        </v-col>
                        <v-col cols="12">
                          <v-text-field
                            v-model="editedItem.product"
                            label="Item Name"
                            outlined
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-text-field
                            v-model="editedItem.price"
                            label="Price"
                            outlined
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-text-field
                            v-model="editedItem.rekening"
                            label="Unit"
                            outlined
                          ></v-text-field>
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
