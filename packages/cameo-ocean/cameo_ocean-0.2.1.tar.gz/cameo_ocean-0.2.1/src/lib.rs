use std::env;
use std::fs;

use actix_cors::Cors;
use actix_files;
use actix_web::{App, HttpRequest, HttpResponse, HttpServer, post, get, Responder};
use actix_web::http::header::HeaderMap;
use pyo3::prelude::*;

use reuse::{append_file, date, date_hour_min, touch};

mod reuse;
mod compression;

fn mkdir(directory: &String) {
    fs::create_dir_all(directory).expect("err lib.rs mkdir")
}

#[get("/api/hi/")]
async fn hi() -> impl Responder {
    HttpResponse::Ok().body("hi rust")
}

#[post("/api/log_msgpack/")]
async fn log_msgpack(req: HttpRequest, body: String) -> impl Responder {
    let map_header = req.headers();
    let mut result: String = "{".to_string();
    result.push_str(r#""headers":""#);
    for key in map_header.keys() {
        reuse::append_str(&mut result, map_header, key.as_str());
    }
    result.push_str(r#"","body":"#);
    result.push_str(&body);
    result.push_str(r#"}"#);
    let bytes = reuse::json_to_bytes(&result);

    let directory = format!("./data/log_msgpack/{}/", date());
    let filename = format!("{}.msgpack", date_hour_min());
    mkdir(&directory);
    let path = format!("{}{}", directory, filename);
    touch(&path);
    append_file(&path, &bytes);
    HttpResponse::Ok().body(path)
}

#[post("/api/echo/")]
async fn echo(body: String) -> impl Responder {
    HttpResponse::Ok().body(body)
}

#[actix_rt::main]
#[pyfunction]
async fn actix_server(host: &str, int_port: usize) -> std::io::Result<()> {
    print_current_directory();
    print_cli();
    let http_server = HttpServer::new(|| {
        App::new()
            .wrap(
                Cors::default()
                    .send_wildcard()
                    .allow_any_method()
                    .allow_any_header()
                    .allow_any_origin()
                    .max_age(3600),
            )
            .service(log_msgpack)
            .service(hi)
            .service(echo)
            .service(actix_files::Files::new("/data/", "./data/").show_files_listing())
    });
    http_server
        .bind(reuse::concat_host_port(host, int_port))?
        .run()
        .await
}

fn print_current_directory() {
    let path = env::current_dir();
    println!("The current directory is {:?}", path);
}

fn print_cli() {
    println!("sh/curl.sh");
}

#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pymodule]
fn cameo_ocean(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(actix_server, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[allow(dead_code)]
fn bad_add(a: i32, b: i32) -> i32 {
    a - b
}

#[cfg(test)]
mod tests {
    use crate::reuse::ls;

    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(1, 2), 3);
    }

    #[test]
    fn test_ls() {
        print!("debug 002 ls {:?}", ls("./data/log_msgpack/2022-05-01/"));
    }
}