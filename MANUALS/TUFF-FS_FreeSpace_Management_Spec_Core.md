# TUFF-FS Free Space Management (Allocator) Technical Specification

## 1. Overview
Free space management in TUFF-FS is implemented as a two-layer structure consisting of a "Bitmap" to manage physical block usage and "Epoch-aware Reclaim" to ensure transactional integrity.

## 2. Physical Block Bitmap
Assigns 1 bit per 4KB physical block of the entire storage to manage usage status.

- **Placement**: Located in the "Bitmap Zone" defined by the `Genesis` block.
- **Loading**: Cached on ZRAM at boot for high-speed allocation via bitwise operations.
- **3N Redundancy**: Independent bitmaps exist for each of the three physical disks. Different physical LBAs are selected for each replica based on the `MetadataCriticalPlacementPolicy`.

## 3. Allocation Lifecycle

### 3.1. Block Reservation
When a write occurs, the allocator searches the bitmap for free blocks and marks them as "Reserved".
At this point, the persistence layer (physical disk) of the bitmap is not updated; it is managed in memory within the UQ (Unique Queue).

### 3.2. Finalization (Commit)
Upon execution of `fs commit` (Epoch flip), the reserved blocks are formally marked as "Allocated" and persisted to the bitmap on disk.

### 3.3. Deferred Reclaim
The most distinctive feature of TUFF-FS. Blocks no longer needed due to deletion or updates are **not immediately returned to the free pool.**

- **ReclaimPendingEntry**: Obsolete blocks are queued in this list along with the Epoch ID in which they became unnecessary.
- **Reuse Conditions**: To preserve J-Generation (Journaling) integrity, blocks are protected in a reserved state until the configured retention period (`MqRetentionPolicy`) and number of Epochs have passed.
- **ReaderTracking**: If there is an active read process via `ActiveChunkRead`, reclamation is further deferred until the process completes.

## 4. Key Structures (tuff-core/src/fs_structs.rs)

| Structure | Role |
|:---|:---|
| `ReclaimState` | Manages the pending reclamation list (`reclaim_pending_list`) and immediate free list (`free_list`). |
| `ReclaimPendingEntry` | Holds the block ID, discarded Epoch, and the Epoch at which reuse is permitted. |
| `ReaderReclaimPolicy` | Defines protection policies for when active read sessions exist. |
| `MetadataCriticalPlacementPolicy` | Determines physical sector strides and slots during 3N redundancy replication. |

## 5. Fault Tolerance
- **Bitmap Inconsistency**: During `fs fsck`, the system cross-checks the bitmap against actual FMC (File Metadata Chunk) pointers to automatically repair dangling blocks or double-allocations.
- **Isolation Mode**: If the system enters Isolation Mode, the allocator refuses all new reservations and physically locks bitmap updates.

## 6. Conclusion
The TUFF-FS allocator is not merely a "free space finder" but functions as an intelligent timeline management mechanism that **safely rotates the reuse cycle while physically protecting J-Generation history.**
