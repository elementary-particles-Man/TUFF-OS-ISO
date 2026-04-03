# TUFF-OS Comprehensive Manual Index (English, v1.1.0)

## 1. Overview and Introduction
- [TUFF-OS General Manual](TUFF-OS_General_Manual.md) — Project philosophy and basic architecture.
- [TUFF-OS Installation Guide (User Edition)](TUFF-OS_Installation_Guide_User.md) — Deployment and initial setup.

## 2. Security Features and Technical Details
- [TUFF-OS Security Features List](TUFF-OS_Security_Features_List.md) — Holistic view of multi-layered defense.
- [TUFF-OS Security Implementation Overview Diagram](TUFF-OS_Security_Implementation_Overview_Diagram.md) — Visual architectural diagrams.
- [TUFF-OS Detailed Technical Manual](TUFF-OS_Detailed_Technical_Manual.md) — Deep dive into the physical layer and asynchronous runtime.
- [TUFF-OS Isolation Mode: Detailed Explanation](TUFF-OS_Isolation_Mode_Deep_Dive.md) — Mechanics of the final line of defense.
- [Isolation Mode Operational Examples](Isolation_Mode_Operational_Examples.md) — Real-world attack response scenarios.

## 3. Storage and File System (TUFF-FS)
- [TUFF-FS Free Space Management (Allocator) Detailed Specification](TUFF-FS_FreeSpace_Management_Detail_JP_EN.md) — Epoch-aware reclamation mechanics.
- [TUFF-FS Emergency Area Specification](TUFF-FS_Emergency_Area_Spec.md) — Automatic evacuation during disk failures.
- [Performance and Integrity Verification](Performance_and_Integrity_Verification.md) — Benchmark data from 2,000-file write tests.

## 4. Operations, Maintenance, and Recovery
- [tuffutl Command Reference (for Users & Admins) v1.1.0](tuffutl_Command_Reference_User_Admin_v1.0.md) — Basic operation guide.
- [tuffutl Command Reference & Backend Specifications (v1.1.0)](tuffutl_Command_Reference_Backend_Specs_v1.0.md) — Reference for developers and power users.
- [tuffutl Web-UI User Reference](tuffutl_Web-UI_User_Reference.md) — Guide for browser-based operations.
- [Backup Creation: Recommended Procedures](Backup_Creation_Recommended_Order.md) — Data preservation methods.
- [Backup and Restore Procedures (Step-by-Step)](Backup_and_Restore_Procedures_Step_by_Step.md) — Detailed restoration steps.
- [TUFF-OS Uninstallation Guide](TUFF-OS_Uninstallation_Guide.md) — Total system deletion procedures.
- [TUFF-OS Isolation Mode: Recovery Procedures](TUFF-OS_Isolation_Mode_Recovery_Procedures.md) — Recovering from an isolated state.
- [TUFF-OS Isolation Mode: Recovery Procedure for Lost PIN](TUFF-OS_Isolation_Mode_PIN_Loss_Recovery_Full.md) — Reinstallation procedure for emergencies.
- [TUFF-OS Troubleshooting Guide](TUFF-OS_Troubleshooting_Guide.md) — Common issues and solutions.

---

## Third-Party API and Trademark Notice

This product may use a compute backend built on the Vulkan API where available.

Vulkan is a registered trademark of The Khronos Group Inc.

The Khronos Group Inc. is not the developer, vendor, maintainer, support provider, certifier, or end-user operator of this product. The Khronos Group Inc. does not endorse this product, and is not responsible for this product’s design, implementation, operation, maintenance, support, safety, security, regulatory status, or any direct or indirect results arising from its use.

Any optional Vulkan-based backend in this product is provided solely by this product’s own developers and distributors. Unless explicitly stated otherwise under separately satisfied Khronos requirements, this product does not claim Khronos conformance, Khronos compliance, Khronos certification, official Vulkan support status, or any other Khronos approval.

For license and attribution details regarding any redistributed third-party components, see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [TRADEMARKS.md](TRADEMARKS.md).
