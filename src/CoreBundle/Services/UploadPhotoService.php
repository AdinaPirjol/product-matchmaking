<?php
namespace CoreBundle\Services;

class UploadPhotoService {

    /**Method called from the controller when the user sends the picture and the category
     * It writes the photo to server
     * On success, the method returns a success string, the category id, the name of the newly file added to server
     * and its location
     * On failure, the method returns "Unable to save this image."
     *
     * @return string
     */

    public function ajax() {
        if (isset($_POST["image"]) && !empty($_POST["image"])) {
            $dataURL = $_POST["image"];
            $selected = $_POST["select"];
        }

        $save_dir = "bundles/core/user_uploads/";

        // the dataURL has a prefix (mimetype+datatype)
        // that we don't want, so strip that prefix off
        $parts = explode(',', $dataURL);
        $data = $parts[1];

        // Decode base64 data, resulting in an image
        $data = base64_decode($data);

        // create a temporary unique file name
        $file = $save_dir . uniqid() . ".png";
        $picture_name = explode("/", $file);

        // write the file to the upload directory
        $success = file_put_contents($file, $data);

        // return the temp file name (success) or return an error message
        if ($success)
            return "Success!###!" . $selected . "###!" . $picture_name[count($picture_name)-1] .
                "###!" . $save_dir . $picture_name[count($picture_name)-1];
        else
            return "Unable to save this image.";
    }

}
