import axios from 'axios';

export type KeyedObject = {
  [key: string]: string | number | null | undefined | KeyedObject | any;
};

const REQUEST_SO_API_URL = 'http://127.0.0.1:8000/requestso/';

// Fetch all requestso data (READ)
export const fetchRequestSOs = async (): Promise<KeyedObject[]> => {
  try {
    const response = await axios.get(REQUEST_SO_API_URL);
    console.log('API Response:', response.data); // Log respons API
    return response.data.map((item: any) => ({
      id: item.RequestSO_ID || '-',
      orderDate: item.OrderDate || '-',
      customerName: item.CustomerName || '-',
      customerNPWP: item.CustomerNPWP || '-',
      customerAddress: item.CustomerAddress || '-',
      customerPhone: item.CustomerPhone || '-',
      itemName: item.ItemName_view || '-',
      itemDesc: item.ItemDesc_view || '-',
      itemPrice: item.ItemPrice_view || '-',
      itemQty: item.ItemQty_view || '-',
      totalPriceperItem: item.TotalPricePerItem_view || '-',
      additionalprice: item.AdditionalPrice_view || '-',
      totalpricebeforeppn: item.TotalPriceBeforePPn_view || '-',
      ppnpercent: item.PPnPercent_view || '-',
      ppnprice: item.PPnPrice_view || '-',
      totalpriceafterppn: item.TotalPriceAfterPPn_view || '-',
      customerBankAccount: item.CustomerBankAccount || '-',
      paymentStatus: item.PaymentStatus || '-',
      paymentProof: item.PaymentProof || '-',
      submissionUser: item.SubmissionUser || '-',
      submissionNotes: item.SubmissionNotes || '-',
      verificationStatus: item.VerificationStatus || '-',
      verificationUser: item.VerificationUser || '-',
      verificationNotes: item.VerificationNotes || '-',
    }));
  } catch (error) {
    console.error('Error fetching requestso data:', error);
    throw new Error('Failed to fetch requestso data');
  }
};

// Add a new requestso data (INSERT)
export const addRequestSO = async (newRequestSO: KeyedObject): Promise<void> => {
  try {
    const response = await axios.post(REQUEST_SO_API_URL, {
      orderdate: newRequestSO.orderdate, // Purchase date
      customerdata: newRequestSO.customerdata, // Customer data
      itemname: newRequestSO.itemname, // Item names concatenated by '|'
      itemdesc: newRequestSO.itemdesc, // Item descriptions concatenated by '|'
      itemprice: newRequestSO.itemprice, // Item prices concatenated by '|'
      itemunit: newRequestSO.itemunit, // Item units concatenated by '|'
      itemqty: newRequestSO.itemqty, // Item quantities concatenated by '|'
      itemaddprice: newRequestSO.itemaddprice, // Additional price
      ppn: newRequestSO.ppn, // Tax percentage
      submitnotes: newRequestSO.submitnotes, // Submission notes
    });
    console.log('Response from server:', response.data);
  } catch (error) {
    console.error('Error adding requestso data:', error);
    throw new Error('Failed to add requestso data');
  }
};

// Update a requestso data (UPDATE)
export const updateRequestSO = async (soId: string, data: Record<string, string | null>): Promise<void> => {
  console.log('Sending update request for SO ID:', soId, 'with data:', data);
  try {
    const url = `http://127.0.0.1:8000/updaterequestso/`;
    await axios.put(url, {
      soid: soId,
      paymentproof: data.paymentProof,
      paymentstatus: data.paymentStatus,
      verifstatus: data.verificationStatus,
      verifnotes: data.verificationNotes,
    });
    console.log('Update successful');
  } catch (error) {
    console.error('Error updating requestso data:', error);
    throw new Error('Failed to update requestso data');
  }
};

// Delete a requestso data (DELETE)
export const deleteRequestSO = async (soId: string): Promise<void> => {
  try {
    await axios.delete(REQUEST_SO_API_URL, {
      data: {
        soid: soId,
        adminid: '01700551', // Admin ID untuk audit log
      },
    });
  } catch (error) {
    console.error('Error deleting requestso data:', error);
    throw new Error('Failed to delete requestso data');
  }
};
