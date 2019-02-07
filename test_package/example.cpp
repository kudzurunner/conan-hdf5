#include <iostream>
#include <hdf5.h>

int main() {
    hid_t file_id = H5Fcreate("example.h5", H5F_ACC_EXCL, H5P_DEFAULT, H5P_DEFAULT);
    if(file_id < 0) {
        std::cout << "Error creating hdf5 file" << std::endl;
        return 1;
    }

    H5Fclose(file_id);
    return 0;
}
