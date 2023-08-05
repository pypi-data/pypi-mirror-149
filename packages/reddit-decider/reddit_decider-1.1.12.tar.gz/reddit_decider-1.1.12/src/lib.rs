use decider::init_decider;
use decider::Context;
use decider::Decider;
use decider::Decision;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pythonize::pythonize;

#[pyclass]
pub struct PyDecider {
    decider: Option<Decider>,
    err_str: Option<String>,
}

#[pyclass]
pub struct PyContext {
    context: Context,
    err_str: Option<String>,
}

#[pymethods]
impl PyContext {
    pub fn inspect(&self) -> String {
        return format!("err: {:#?} \ncontext: {:#?}", self.err_str, self.context);
    }

    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }
}

#[pyclass]
pub struct GetExperimentRes {
    val: Option<Py<PyAny>>,
    pub err_str: Option<String>,
}

#[pymethods]
impl GetExperimentRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err_str, self.val)
    }

    pub fn val(&mut self) -> Option<Py<PyAny>> {
        self.val.clone()
    }

    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }
}

#[pyclass]
pub struct GetBoolRes {
    val: bool,
    err_str: Option<String>,
}

#[pymethods]
impl GetBoolRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err_str, self.val)
    }

    pub fn val(&self) -> bool {
        self.val
    }

    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }
}

#[pyclass]
pub struct GetIntegerRes {
    val: i64,
    err_str: Option<String>,
}

#[pymethods]
impl GetIntegerRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err_str, self.val)
    }

    pub fn val(&self) -> i64 {
        self.val
    }

    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }
}

#[pyclass]
pub struct GetFloatRes {
    val: f64,
    err_str: Option<String>,
}

#[pymethods]
impl GetFloatRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err_str, self.val)
    }

    pub fn val(&self) -> f64 {
        self.val
    }

    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }
}

#[pyclass]
pub struct GetStringRes {
    val: String,
    err_str: Option<String>,
}

#[pymethods]
impl GetStringRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err_str, self.val)
    }

    pub fn val(&self) -> String {
        self.val.clone()
    }

    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }
}

#[pyclass]
pub struct GetMapRes {
    val: Py<PyAny>,
    err_str: Option<String>,
}

#[pymethods]
impl GetMapRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err_str, self.val)
    }

    pub fn val(&self) -> Py<PyAny> {
        self.val.clone()
    }

    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }
}

#[pyclass]
pub struct PyDecision {
    decision: Option<Decision>,
    err_str: Option<String>,
}

#[pymethods]
impl PyDecision {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, decision: {:?}", self.err_str, self.decision)
    }

    pub fn decision(&self) -> Option<String> {
        self.decision.as_ref().and_then(|d| d.name.clone())
    }

    pub fn events(&self) -> Vec<String> {
        match &self.decision {
            None => vec![],
            Some(d) => d.event_data.clone(),
        }
    }

    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }
}

#[pymethods]
impl PyDecider {
    pub fn err(&self) -> Option<String> {
        self.err_str.clone()
    }

    pub fn choose(&self, feature_name: String, ctx: &PyContext) -> Option<PyDecision> {
        match &self.decider {
            Some(decider) => match decider.choose(feature_name, &ctx.context) {
                Ok(res) => Some(PyDecision {
                    decision: res,
                    err_str: None,
                }),
                Err(e) => Some(PyDecision {
                    decision: None,
                    err_str: Some(e.to_string()),
                }),
            },
            None => Some(PyDecision {
                decision: None,
                err_str: Some("Decider not found.".to_string()),
            }),
        }
    }

    pub fn get_experiment(&self, feature_name: String) -> GetExperimentRes {
        match &self.decider {
            Some(decider) => match decider.feature_by_name(feature_name) {
                Ok(feature) => {
                    let gil = Python::acquire_gil();
                    let py = gil.python();
                    match pythonize(py, &feature) {
                        Ok(pydict) => GetExperimentRes {
                            val: Some(pydict),
                            err_str: None,
                        },
                        Err(e) => GetExperimentRes {
                            val: None,
                            err_str: Some(e.to_string()),
                        },
                    }
                }
                Err(e) => GetExperimentRes {
                    val: None,
                    err_str: Some(e.to_string()),
                },
            },
            None => GetExperimentRes {
                val: None,
                err_str: Some("Decider not found.".to_string()),
            },
        }
    }

    pub fn get_bool(&self, feature_name: String, ctx: &PyContext) -> GetBoolRes {
        match &self.decider {
            Some(decider) => match decider.get_bool(feature_name, &ctx.context) {
                Ok(b) => GetBoolRes {
                    val: b,
                    err_str: None,
                },
                Err(e) => GetBoolRes {
                    val: false,
                    err_str: Some(e.to_string()),
                },
            },
            None => GetBoolRes {
                val: false,
                err_str: Some("Decider not found.".to_string()),
            },
        }
    }

    pub fn get_int(&self, feature_name: String, ctx: &PyContext) -> GetIntegerRes {
        match &self.decider {
            Some(decider) => match decider.get_int(feature_name, &ctx.context) {
                Ok(i) => GetIntegerRes {
                    val: i,
                    err_str: None,
                },
                Err(e) => GetIntegerRes {
                    val: 0,
                    err_str: Some(e.to_string()),
                },
            },
            None => GetIntegerRes {
                val: 0,
                err_str: Some("Decider not found.".to_string()),
            },
        }
    }

    pub fn get_float(&self, feature_name: String, ctx: &PyContext) -> GetFloatRes {
        match &self.decider {
            Some(decider) => match decider.get_float(feature_name, &ctx.context) {
                Ok(f) => GetFloatRes {
                    val: f,
                    err_str: None,
                },
                Err(e) => GetFloatRes {
                    val: 0.0,
                    err_str: Some(e.to_string()),
                },
            },
            None => GetFloatRes {
                val: 0.0,
                err_str: Some("Decider not found.".to_string()),
            },
        }
    }

    pub fn get_string(&self, feature_name: String, ctx: &PyContext) -> GetStringRes {
        match &self.decider {
            Some(decider) => match decider.get_string(feature_name, &ctx.context) {
                Ok(s) => GetStringRes {
                    val: s,
                    err_str: None,
                },
                Err(e) => GetStringRes {
                    val: "".to_string(),
                    err_str: Some(e.to_string()),
                },
            },
            None => GetStringRes {
                val: "".to_string(),
                err_str: Some("Decider not found.".to_string()),
            },
        }
    }

    pub fn get_map(&self, feature_name: String, ctx: &PyContext) -> GetMapRes {
        let gil = Python::acquire_gil();
        let py = gil.python();
        match &self.decider {
            Some(decider) => {
                let res = decider.get_map(feature_name, &ctx.context);
                match res {
                    Ok(val) => match pythonize(py, &val) {
                        Ok(pydict) => GetMapRes {
                            val: pydict,
                            err_str: None,
                        },
                        Err(e) => {
                            let pany: Py<PyAny> = PyDict::new(py).into();
                            GetMapRes {
                                val: pany,
                                err_str: Some(e.to_string()),
                            }
                        }
                    },
                    Err(e) => {
                        let pany: Py<PyAny> = PyDict::new(py).into();
                        GetMapRes {
                            val: pany,
                            err_str: Some(e.to_string()),
                        }
                    }
                }
            }
            None => {
                let pany: Py<PyAny> = PyDict::new(py).into();
                GetMapRes {
                    val: pany,
                    err_str: Some("Decider not found.".to_string()),
                }
            }
        }
    }
}

#[pyfunction]
pub fn init(decisionmakers: String, filename: String) -> PyDecider {
    match init_decider(decisionmakers, filename) {
        Ok(dec) => PyDecider {
            decider: Some(dec),
            err_str: None,
        },
        Err(e) => PyDecider {
            decider: None,
            err_str: Some(e.to_string()),
        },
    }
}

#[pyfunction]
pub fn make_ctx(ctx_dict: &PyDict) -> PyContext {
    let mut err_vec: Vec<String> = Vec::new();

    let user_id = match extract_field::<String>(ctx_dict, "user_id", "string") {
        Ok(u_id) => match u_id {
            Some(id) => id,
            None => {
                err_vec.push("'user_id' field missing.".to_string());
                "".to_string()
            }
        },
        Err(e) => {
            err_vec.push(e);
            "".to_string()
        }
    };

    let locale: Option<String> = match extract_field::<String>(ctx_dict, "locale", "string") {
        Ok(loc) => loc,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let device_id = match extract_field::<String>(ctx_dict, "device_id", "string") {
        Ok(d_id) => d_id,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let canonical_url = match extract_field::<String>(ctx_dict, "canonical_url", "string") {
        Ok(c_url) => c_url,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let country_code = match extract_field::<String>(ctx_dict, "country_code", "string") {
        Ok(cc) => cc,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let origin_service = match extract_field::<String>(ctx_dict, "origin_service", "string") {
        Ok(os) => os,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let user_is_employee = match extract_field::<bool>(ctx_dict, "user_is_employee", "bool") {
        Ok(uie) => uie,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let logged_in = match extract_field::<bool>(ctx_dict, "logged_in", "bool") {
        Ok(li) => li,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let app_name = match extract_field::<String>(ctx_dict, "app_name", "string") {
        Ok(an) => an,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let build_number = match extract_field::<i32>(ctx_dict, "build_number", "integer") {
        Ok(bn) => bn,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let auth_client_id =
        match extract_field::<String>(ctx_dict, "auth_client_id", "string") {
            Ok(at) => at,
            Err(e) => {
                err_vec.push(e);
                None
            }
        };

    let cookie_created_timestamp =
        match extract_field::<f64>(ctx_dict, "cookie_created_timestamp", "float") {
            Ok(cct) => cct,
            Err(e) => {
                err_vec.push(e);
                None
            }
        };

    PyContext {
        context: Context {
            user_id,
            locale,
            device_id,
            canonical_url,
            country_code,
            origin_service,
            user_is_employee,
            logged_in,
            app_name,
            build_number,
            auth_client_id,
            cookie_created_timestamp,
        },
        err_str: match err_vec.len() {
            0 => None,
            _ => Some(err_vec.join("\n")),
        },
    }
}

fn extract_field<T>(ctx_dict: &PyDict, key: &str, field_type: &str) -> Result<Option<T>, String>
where
    T: for<'p> FromPyObject<'p>,
{
    match ctx_dict.get_item(key) {
        Some(val) => {
            if val.is_none() {
                Ok(None)
            } else {
                match val.extract::<T>() {
                    Ok(s) => Ok(Some(s)),
                    _ => Err(format!("{:#?} type mismatch ({:}).", key, field_type)),
                }
            }
        }
        None => Ok(None),
    }
}

#[pymodule]
fn rust_decider(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(make_ctx, m)?)?;

    Ok(())
}
