# TUFF-OS LiveUSB リポジトリ

このリポジトリには、TUFF-OS の LiveUSB 用インストールイメージおよびリリース成果物が含まれています。

## TUFF-OS 2段階インストール・アーキテクチャ

TUFF-OS は、以下の2段階の手順で実機へインストールされます。これにより、UEFI 起動の確立と、ハードウェアリソース（8MB キュー等）の厳密なマッピングを両立します。

### 1. 第1段階: TUFF-INSTALL-UEFI (UEFI の全把握)
- **役割**: 実機のマザーボードおよび SSD の EFI 領域に対し、TUFF-OS の起動起点（`TUFFboot.efi`）を確立します。
- **実行**: インストールメディアから起動し、SSD の EFI パーティションに `TUFFboot.efi` を配置します。
- **サイズ**: 実体は数 MB の最小限のフットプリントです。不必要な巨大イメージの生成は行いません。

### 2. 第2段階: TUFF-INSTALL-MAIN (システム展開と参加)
- **役割**: すでに起動している `TUFF-OS-UEFI` の制御下で、OS 本体の展開とリソースマッピングを行います。
- **実行**: 
  - `TUFF-KERNEL` (めっちゃちっちゃいファイル) を SSD に配置。
  - **各 HDD に対応する 8MB キュー** をメモリ/ディスク上に論理的にマッピングし、物理的に初期化します。
  - Snappy/LZ4 圧縮プール（Sovereign ZRAM）の定義を確定させます。

---

## 配布
- **バージョン**: 1.1.0 (LiveUSB インストーラ版)
- **ターゲット**: x86_64 UEFI 準拠
- **最新イメージ**: `latest/TUFF-OS-latest.iso`

## インストール手順
1. `TUFF-OS-latest.iso` を USB メモリへ raw 書き込みしてください。
2. 作成した USB から UEFI モードで起動してください。
3. `TUFF-INSTALL-UEFI` (Phase 1) を実行し、起動の起点を確立します。
4. 再起動後、`TUFF-INSTALL-MAIN` (Phase 2) が呼び出され、SSD へのカーネル配置と 8MB キューのマッピングが行われます。

---

## 🚀 徹底的なZRAM圧縮アーキテクチャ (Sovereign ZRAM)
TUFF-OSは、GoogleのSnappy/LZ4アルゴリズムの思想をベアメタルレベルで統合しています。
システムメモリ（Sovereign Heap）の大部分を「インメモリ圧縮プール」として確保し、
Unique Queue (UQ)のデータやファイルシステムのキャッシュを透過的かつ超高速に圧縮・伸張します。
これにより、極端にメモリが少ない環境でも、実質的なメモリ容量を数倍に拡張し、
Vulkan GPUオフロードやPQC（耐量子暗号）の並列処理をリソース枯渇なしに実行し続けます。

The Ultimate Fortress Foundation OS (TUFF-OS) は、従来のカーネルに依存しない、**完全独立型の Pure Rust ベアメタル Sovereign OS** です。UEFIの `ExitBootServices` からシステムを直接掌握し、GDT、IDT、ページングの絶対的な制御権を確立します。

## ライセンス
- 個人、研究、および非商用利用は無償。
- 商用利用には個別契約が必要です。
詳細は [LICENSE](LICENSE) を参照してください。
