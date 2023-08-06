use std::fs;
use std::fs::{DirEntry, OpenOptions};
use std::io::{Error, Write};
use std::path::Path;

use serde_json::Value;
use substring::Substring;

use crate::HeaderMap;

pub fn touch(path: &String) {
    OpenOptions::new()
        .create(true)
        .write(true)
        .open(Path::new(path))
        .expect("err reuse.rs touch()");
}

pub fn append_file(path: &String, bytes: &Vec<u8>) {
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .open(path)
        .expect(&*format!("err reuse.rs append_file, path:{}", path));
    file.write_all(bytes).unwrap();
}

pub fn append_str(result: &mut String, map: &HeaderMap, key: &str) {
    result.push_str(format!("{}: {}\\n", key, map.get(key).unwrap().to_str().unwrap()).as_str());
}

pub fn json_to_bytes(result: &String) -> Vec<u8> {
    let v: Value = serde_json::from_str(&result).unwrap();
    let bytes = rmp_serde::to_vec(&v).unwrap();
    bytes
}

pub fn time_slice(i: usize) -> String {
    format!("{:?}", chrono::offset::Local::now())
        .substring(0, i)
        .replace(":", "_")
        .replace("T", "_")
}

pub fn date() -> String {
    time_slice(10)
}

pub fn date_hour_min() -> String {
    time_slice(16)
}

pub fn concat_host_port(host: &str, int_port: usize) -> String {
    let str_ip_port = format!("{}:{}", host, int_port);
    println!("cameo_ocean actix server at {}", str_ip_port);
    str_ip_port
}

fn _path_to_string(path: Result<DirEntry, Error>) -> String {
    path.unwrap().path().to_str().unwrap().to_string()
}

pub fn _ls(directory: &str) -> Vec<String> {
    let mut v: Vec<String> = Vec::new();
    let paths = fs::read_dir(directory).unwrap();
    for path in paths {
        v.push(_path_to_string(path));
    };
    v
}


