<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;


class UserController extends Controller
{
    public function uploading_page() {
        return view("uploading_page");
    }
    public function output_page() {
        return view("output_page");
    }
}
