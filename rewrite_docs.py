import os
import re

TARGET_DIRS = [
    ".",
    "MANUALS",
    "マニュアル"
]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # --- JAPNESE & GENERAL REPLACEMENTS ---
    content = re.sub(r'Linux\s*kernel', 'TUFF-KERNEL (Pure Rust Bare-metal Sovereign Core)', content, flags=re.IGNORECASE)
    content = re.sub(r'Linux\s*カーネル', 'TUFF-KERNEL (Pure Rust Bare-metal Sovereign Core)', content)
    content = re.sub(r'bzImage', 'tuff-kernel.efi (Pure Rust Bare-metal Executable)', content)
    
    content = re.sub(r'上位OS（Windows\s*/\s*Linux\s*/\s*macOS等）の\**下位レイヤー\**で稼働するセキュリティ基盤OS', 'UEFIから直接システムを掌握し、ExitBootServicesを経てハードウェアを完全制御するPure RustベアメタルOS', content)
    content = re.sub(r'上位OS', 'アプリケーション層', content)
    
    content = re.sub(r'ハイパーバイザ', 'ベアメタル Sovereign Executive', content)
    content = re.sub(r'Hypervisor', 'Bare-metal Sovereign Executive', content, flags=re.IGNORECASE)

    content = re.sub(r'ランタイム管理型非同期ランタイム', 'Sovereign Executive & Async Runtime', content)
    content = re.sub(r'ホットパスでランタイム管理型のスケジューリングと固定長のセッション/状態構造を用います。タスクの起床（Wake）は `AtomicU32` のビットマップ通知によって行われ、割り込み（IRQ）からO\(1\)の定数時間でタスクを再開します。', 'ハードウェアタイマー (IRQ0) 駆動の独自非同期エグゼキュータ (Sovereign Executive) と `SleepFuture` を用い、ホストOSに依存しない真のマルチタスクとOS Tickを実現します。タスクの起床はIRQから直接O(1)で処理され、極めて低いレイテンシを誇ります。', content)
    
    content = re.sub(r'論理的なファイルシステムの脆弱性を排除し', '4階層ページテーブルとNX (No-Execute) ビットによる物理ハードウェアレベルのメモリ保護を強制し、論理的な脆弱性を排除し', content)

    content = re.sub(r'Vulkan GPGPU オフロード', 'ベアメタル Vulkan GPGPU オフロード (PCIe BARs 直接アクセス)', content)
    content = re.sub(r'iGPUへオフロードし、CPU使用率0.0%のまま攻撃を無効化します。', 'PCIe BARs経由でSovereign Command Ringからコンピュートシェーダを直接GPUへサブミットし、CPU使用率を限りなく0.0%に近づけながら攻撃を無効化します。', content)

    content = re.sub(r'AVX2\s*/\s*AVX-512の256/512-bit\s*SIMD', 'OSスケジューラによってネイティブ管理されるAVX/AVX-512ベクトル命令', content)
    content = re.sub(r'AVX2の8レーン並列処理', 'OS管理下のAVX/AVX-512ベクトル命令', content)

    # --- ENGLISH REPLACEMENTS ---
    content = re.sub(r'underlying OS \(Windows / Linux / macOS, etc\.\)', 'Pure Rust Bare-metal OS taking direct control from UEFI', content, flags=re.IGNORECASE)
    content = re.sub(r'upper OS', 'application layer', content, flags=re.IGNORECASE)
    content = re.sub(r'upper level OS', 'application layer', content, flags=re.IGNORECASE)
    content = re.sub(r'host OS', 'application layer', content, flags=re.IGNORECASE)
    content = re.sub(r'runtime-managed async runtime', 'Sovereign Executive & Async Runtime', content, flags=re.IGNORECASE)
    
    # General Intro in EN
    content = content.replace(
        "The Ultimate Fortress Foundation OS (TUFF-OS) is a security-focused OS that provides absolute data sovereignty at the physical layer.",
        "The Ultimate Fortress Foundation OS (TUFF-OS) is a **Pure Rust Bare-metal Sovereign OS**, completely independent of Linux or any legacy kernel. By taking direct control from UEFI via `ExitBootServices`, it asserts absolute dominance over the GDT, IDT, and Paging. It provides absolute data sovereignty at the physical layer, enforced by Hardware-Native Security (NX-Bit & 4-level page tables), and extreme performance via bare-metal GPU and AVX orchestration."
    )
    
    # General Intro in JP
    content = content.replace(
        "The Ultimate Fortress Foundation OS (TUFF-OS) は、物理層での絶対的なデータ主権を提供するセキュリティ特化型 OS です。",
        "The Ultimate Fortress Foundation OS (TUFF-OS) は、Linuxや従来のカーネルに依存しない、**完全独立型の Pure Rust ベアメタル Sovereign OS** です。UEFIの `ExitBootServices` からシステムを直接掌握し、GDT、IDT、ページングの絶対的な制御権を確立します。物理層での絶対的なデータ主権と、ベアメタルGPU/AVXオーケストレーションによる極限のパフォーマンスを提供します。"
    )

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_path = '/media/flux/THPDOC/Develop/TUFF-OS/TUFF-OS-LiveUSB'
    changed_files = []
    
    for d in TARGET_DIRS:
        dp = os.path.join(base_path, d)
        if not os.path.exists(dp):
            continue
        # We only want to process the top level and MANUALS / マニュアル directories
        if d == ".":
            files = [f for f in os.listdir(dp) if os.path.isfile(os.path.join(dp, f)) and f.endswith('.md')]
            for f in files:
                filepath = os.path.join(dp, f)
                if process_file(filepath):
                    changed_files.append(filepath)
        else:
            for root, dirs, files in os.walk(dp):
                for f in files:
                    if f.endswith('.md'):
                        filepath = os.path.join(root, f)
                        if process_file(filepath):
                            changed_files.append(filepath)
                        
    print(f"Updated {len(changed_files)} files.")

if __name__ == '__main__':
    main()
