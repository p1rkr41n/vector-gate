pub mod config;
pub mod engine;
pub mod splice;

pub use config::*;
pub use engine::*;
pub use splice::*;

use std::path::Path;

/// Check configuration files and start any declared gates on the provided Tokio runtime handle
pub fn maybe_start_gates_from_paths<P: AsRef<Path>>(paths: &[P], handle: &tokio::runtime::Handle) {
    for path in paths {
        let p = path.as_ref();
        if let Ok(content) = std::fs::read_to_string(p) {
            if content.contains("gates:") {
                if engine::maybe_start_gates_from_config(&content, handle) {
                    println!("🛡️ [Vector Smart Gate] Ingress engine active for config: {}", p.display());
                }
            }
        }
    }
}
