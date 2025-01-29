import axios from 'axios';

export type KeyedObject = {
  [key: string]: string | number | null | undefined | KeyedObject | any;
};

const REQUEST_PO_API_URL = 'http://127.0.0.1:8000/requestpo/';

// Fetch all requestpo data (READ)
export const fetchRequestPOs = async (): Promise<KeyedObject[]> => {
  try {
    const response = await axios.get(REQUEST_PO_API_URL);
    return response.data.map((item: any) => ({
      id: item.RequestPO_ID || '',
      orderDate: item.OrderDate || '',
      vendorName: item.VendorName || '',
      vendorAddress: item.VendorAddress || '',
      vendorPhone: item.VendorPhone || '',
      itemName: item.ItemName_view || '',
      itemDesc: item.ItemDesc_view || '',
      itemPrice: item.ItemPrice_view || '',
      itemQty: item.ItemQty_view || '',
      totalPrice: item.SubTotalPrice_view || '',
      alltotalPrice: item.TotalPrice_view || '',
      vendorBankAccount: item.VendorBankAccount || '',
      paymentStatus: item.PaymentStatus || '',
      paymentProof: item.PaymentProof || '',
      submissionUser: item.SubmissionUser || '',
      submissionNotes: item.SubmissionNotes || '',
      verificationStatus: item.VerificationStatus || '',
      verificationUser: item.VerificationUser || '',
      verificationNotes: item.VerificationNotes || '',
    }));
  } catch (error) {
    console.error('Error fetching requestpo data from API:', error);
    throw new Error('Failed to fetch requestpo data');
  }
};

// Add a new requestpo data (INSERT)
export const addRequestPO = async (newRequestPO: KeyedObject): Promise<void> => {
  try {
    await axios.post(REQUEST_PO_API_URL, {
      orderdate: newRequestPO.orderdate,
      vendordata: newRequestPO.vendordata,
      itemname: newRequestPO.itemname,
      itemdesc: newRequestPO.itemdesc,
      itemprice: newRequestPO.itemprice,
      itemunit: newRequestPO.itemunit, // Tambahkan itemunit
      itemqty: newRequestPO.itemqty,
      submitnotes: newRequestPO.submitnotes,
    });
  } catch (error) {
    console.error('Error adding requestpo data:', error);
    throw new Error('Failed to add requestpo data');
  }
};

export const updateRequestPO = async (poId: string, data: Record<string, string | null>): Promise<void> => {
  console.log('Sending update request for PO ID:', poId, 'with data:', data);
  try {
    const url = `http://127.0.0.1:8000/updaterequestpo/`;
    await axios.put(url, {
      poid: poId,
      paymentproof: data.paymentProof,
      paymentstatus: data.paymentStatus,
      verifstatus: data.verificationStatus,
      verifnotes: data.verificationNotes,
    });
    console.log('Update successful');
  } catch (error) {
    console.error('Error updating request PO:', error);
    throw new Error('Failed to update request PO');
  }
};

// Delete a requestpo data (DELETE)
export const deleteRequestPO = async (poId: string): Promise<void> => {
  try {
    await axios.delete(REQUEST_PO_API_URL, {
      data: {
        poid: poId,
        adminid: '01700551',
      },
    });
  } catch (error) {
    console.error('Error deleting requestpo data:', error);
    throw new Error('Failed to delete requestpo data');
  }
};