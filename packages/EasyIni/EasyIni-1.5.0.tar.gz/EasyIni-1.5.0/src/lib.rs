
use pyo3::prelude::*;

// /// Formats the sum of two numbers as string.
// #[pyfunction]
// fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
//     Ok((a + b).to_string())
// }
// #[pyfunction]
// fn getsss(a: String) -> PyResult<String> {
//     Ok(a)
// }
// /// A Python module implemented in Rust.
#[pymodule]
fn EasyIni(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(gget, m)?)?;
    m.add_function(wrap_pyfunction!(sset, m)?)?;
    Ok(())
}
use configparser::ini::Ini;
use std::fs;


#[pyfunction]
pub extern fn gget(words:String,key:String,default:String,defaultfile:String) ->PyResult<String>{
    let mut config = Ini::new();
    if let Ok(_map) = config.load(defaultfile.to_string()){
        if let Some(xx) = config.get(&words.to_string(),&key.to_string()){
            Ok(xx.to_string())
        }else{
            config.load(defaultfile.to_string()).unwrap();
            config.set(&words.to_string(),&key.to_string(),Some(default.to_string()));
            match config.write(defaultfile.to_string()){
                Ok(_)=>println!("ooo"),
                Err(_)=>println!("errorok")
            }
            Ok(default.to_string())
        }
    }else{
        let _file = fs::OpenOptions::new().write(true).append(true).create(true).open(defaultfile.to_string()).unwrap();
        config.load(defaultfile.to_string()).unwrap();
        config.set(&words.to_string(),&key.to_string(),Some(default.to_string()));
        match config.write(defaultfile.to_string()){
            Ok(_)=>println!("ooo"),
            Err(_)=>println!("errorok")
        }
        Ok(default.to_string())
   }
}
#[pyfunction]
pub extern fn sset(words:String,key:String,default:String,defaultfile:String) ->PyResult<bool>{
    let mut config = Ini::new();
    if let Ok(_map) = config.load(&defaultfile){
        if let Some(_xx) = config.set(&words.to_string(),&key.to_string(),Some(default.to_string())){
            match config.write(defaultfile.to_string()){
                Ok(_)=>true,
                Err(_)=>false
            };
            Ok(true)
        }else{
            let _file = fs::OpenOptions::new().write(true).append(true).create(true).open(defaultfile.to_string()).unwrap();
            config.load(defaultfile.to_string()).unwrap();
            config.set(&words.to_string(),&key.to_string(),Some(default.to_string()));
            match config.write(defaultfile.to_string()){
                Ok(_)=>Ok(true),
                Err(_)=>Ok(false)
            }
        }
    }else{
        let _file = fs::OpenOptions::new().write(true).append(true).create(true).open(&defaultfile).unwrap();
        config.load(&defaultfile).unwrap();
        config.set(&words.to_string(),&key.to_string(),Some(default.to_string()));
        match config.write(defaultfile.to_string()){
            Ok(_)=>Ok(true),
            Err(_)=>Ok(false)
        }
   }
}
