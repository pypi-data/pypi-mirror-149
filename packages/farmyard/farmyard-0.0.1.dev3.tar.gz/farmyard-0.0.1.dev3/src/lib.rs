
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: i64, b: i64) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn version() -> PyResult<String> {
    Ok(String::from("0.0.1.dev1"))
}

/// A Python module implemented in Rust.
#[pymodule]
fn _farmyard_native(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    Ok(())
}
