<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;

Route::get('/', function () {
    return view('landing_page');
});

Route::post('/uploading_page' ,[UserController::class,'uploading_page']);
Route::get('/output_page',[UserController::class,'output_page']);