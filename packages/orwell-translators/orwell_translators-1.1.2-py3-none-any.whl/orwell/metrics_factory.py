from .metric import Metric


class MetricsFactory:

  @classmethod
  def create_load_metric (cls, interval: int, value: str, ts: str, instance: str):
    return Metric('node_load' + str(interval), value, { }, ts, instance)

  @classmethod
  def create_cpu_time_metric (cls, cpu: str, mode: str, value: str, ts: str, instance: str):
    return Metric('node_cpu_seconds_total', value, { 'cpu': cpu, 'mode': mode }, ts, instance)

  @classmethod
  def create_filesystem_metric (cls, title: str, device: str, fstype: str, mountpoint: str, value: str, ts: str, instance: str):
    return Metric('node_filesystem_%s_bytes' % (title,), value, { 'device': device, 'fstype': fstype, 'mountpoint': mountpoint }, ts, instance)

  @classmethod
  def create_filesystem_available_metric (cls, device: str, fstype: str, mountpoint: str, value: str, ts: str, instance: str):
    return cls.create_filesystem_metric('avail', device, fstype, mountpoint, value, ts, instance)

  @classmethod
  def create_filesystem_size_metric (cls, device: str, fstype: str, mountpoint: str, value: str, ts: str, instance: str):
    return cls.create_filesystem_metric('size', device, fstype, mountpoint, value, ts, instance)

  @classmethod
  def create_memory_metric (cls, title: str, value: str, ts: str, instance: str):
    return Metric('node_memory_%s_bytes' % (title,), value, {  }, ts, instance)

  @classmethod
  def create_memory_total_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('MemTotal', value, ts, instance)

  @classmethod
  def create_memory_free_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('MemFree', value, ts, instance)

  @classmethod
  def create_memory_available_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('MemAvailable', value, ts, instance)

  @classmethod
  def create_memory_cached_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Cached', value, ts, instance)

  @classmethod
  def create_memory_buffered_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Buffers', value, ts, instance)

  @classmethod
  def create_memory_slab_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Slab', value, ts, instance)

  @classmethod
  def create_memory_page_tables_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('PageTables', value, ts, instance)

  @classmethod
  def create_memory_inactive_metric (cls, value: str, ts: str, instance: str, detail: str = None):
    return cls.create_memory_metric('Inactive%s' % ('' if detail is None else '_' + detail,), value, ts, instance)

  @classmethod
  def create_memory_active_metric (cls, value: str, ts: str, instance: str, detail: str = None):
    return cls.create_memory_metric('Active%s' % ('' if detail is None else '_' + detail,), value, ts, instance)

  @classmethod
  def create_memory_committed_as_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Committed_AS', value, ts, instance)

  @classmethod
  def create_memory_commit_limit_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('CommitLimit', value, ts, instance)

  @classmethod
  def create_memory_swap_metric (cls, title: str, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Swap%s' % (title,), value, ts, instance)

  @classmethod
  def create_memory_swap_total_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_swap_metric('Total', value, ts, instance)

  @classmethod
  def create_memory_swap_free_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_swap_metric('Free', value, ts, instance)

  @classmethod
  def create_memory_vmalloc_metric (cls, title: str, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Vmalloc%s' % (title,), value, ts, instance)

  @classmethod
  def create_memory_vmalloc_chunk_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_vmalloc_metric('Chunk', value, ts, instance)

  @classmethod
  def create_memory_vmalloc_total_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_vmalloc_metric('Total', value, ts, instance)

  @classmethod
  def create_memory_vmalloc_used_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_vmalloc_metric('Used', value, ts, instance)

  @classmethod
  def create_memory_writeback_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Writeback', value, ts, instance)

  @classmethod
  def create_memory_writeback_tmp_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('WritebackTmp', value, ts, instance)

  @classmethod
  def create_memory_dirty_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Dirty', value, ts, instance)

  @classmethod
  def create_memory_mapped_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Mapped', value, ts, instance)

  @classmethod
  def create_memory_reclaimable_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('SReclaimable', value, ts, instance)

  @classmethod
  def create_memory_huge_pages_metric (cls, value: str, ts: str, instance: str, detail: str = None):
    return Metric('node_memory_HugePages_%s' % ('' if detail is None else '_' + detail,), value, {}, ts, instance)

  @classmethod
  def create_memory_huge_pages_free_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_huge_pages_metric(value, ts, instance, 'Free')

  @classmethod
  def create_memory_huge_pages_rsvd_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_huge_pages_metric(value, ts, instance, 'Rsvd')

  @classmethod
  def create_memory_huge_pages_total_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_huge_pages_metric(value, ts, instance, 'Total')

  @classmethod
  def create_memory_direct_map_metric (cls, value: str, ts: str, instance: str, detail: str = None):
    return cls.create_memory_metric('DirectMap%s' % ('' if detail is None else '_' + detail,), value, ts, instance)

  @classmethod
  def create_memory_direct_map_1g_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_direct_map_metric(value, ts, instance, '1G')

  @classmethod
  def create_memory_direct_map_2m_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_direct_map_metric(value, ts, instance, '2M')

  @classmethod
  def create_memory_direct_map_4k_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_direct_map_metric(value, ts, instance, '4k')

  @classmethod
  def create_memory_huge_pages_free_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_huge_pages_metric(value, ts, instance, 'Free')

  @classmethod
  def create_memory_huge_pages_rsvd_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_huge_pages_metric(value, ts, instance, 'Rsvd')

  @classmethod
  def create_memory_huge_pages_total_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_huge_pages_metric(value, ts, instance, 'Total')

  @classmethod
  def create_memory_huge_pages_size_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Hugepagesize', value, ts, instance)

  @classmethod
  def create_memory_unevictable_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Unevictable', value, ts, instance)

  @classmethod
  def create_memory_mlocked_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('Mlocked', value, ts, instance)

  @classmethod
  def create_memory_nfs_metric (cls, value: str, ts: str, instance: str):
    return cls.create_memory_metric('NFS_Unstable', value, ts, instance)

  @classmethod
  def create_up_time_metric (cls, value: str, ts: str, instance: str):
    return Metric('node_time_seconds', value, {  }, ts, instance)

  @classmethod
  def create_boot_time_metric (cls, value: str, ts: str, instance: str):
    return Metric('node_boot_time_seconds', value, {  }, ts, instance)

  @classmethod
  def create_network_bytes_metric (cls, title: str, value: str, ts: str, instance: str):
    return Metric('node_network_%s_bytes_total' % (title,), value, {  }, ts, instance)

  @classmethod
  def create_network_receive_bytes_metric (cls, value: str, ts: str, instance: str):
    return cls.create_network_bytes_metric('receive', value, ts, instance)

  @classmethod
  def create_network_transmit_bytes_metric (cls, value: str, ts: str, instance: str):
    return cls.create_network_bytes_metric('transmit', value, ts, instance)

  @classmethod
  def create_disk_metric (cls, title: str, device: str, value: str, ts: str, instance: str):
    return Metric('node_disk_%s_total' % (title,), value, { 'device': device }, ts, instance)

  @classmethod
  def create_disk_completed_metric (cls, title: str, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_metric('%s_completed' % (title,), device, value, ts, instance)

  @classmethod
  def create_disk_reads_completed_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_completed_metric('reads', device, value, ts, instance)

  @classmethod
  def create_disk_writes_completed_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_completed_metric('writes', device, value, ts, instance)

  @classmethod
  def create_disk_bytes_metric (cls, title: str, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_metric('%s_bytes' % (title,), device, value, ts, instance)

  @classmethod
  def create_disk_read_bytes_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_bytes_metric('read', device, value, ts, instance)

  @classmethod
  def create_disk_written_bytes_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_bytes_metric('written', device, value, ts, instance)

  @classmethod
  def create_disk_io_time_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_metric('io_time_seconds', device, value, ts, instance)

  @classmethod
  def create_disk_io_time_weighted_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_metric('io_time_weighted_seconds', device, value, ts, instance)

  @classmethod
  def create_disk_io_read_time_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_metric('read_time_seconds', device, value, ts, instance)

  @classmethod
  def create_disk_io_reads_merged_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_metric('reads_merged', device, value, ts, instance)

  @classmethod
  def create_disk_io_writes_merged_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_metric('writes_merged', device, value, ts, instance)

  @classmethod
  def create_disk_io_write_time_metric (cls, device: str, value: str, ts: str, instance: str):
    return cls.create_disk_metric('write_time_seconds', device, value, ts, instance)

  @classmethod
  def create_disk_io_now_metric (cls, device: str, value: str, ts: str, instance: str):
    return Metric('node_disk_io_now', value, { 'device': device }, ts, instance)

  @classmethod
  def create_vmstat_metric (cls, title: str, value: str, ts: str, instance: str):
    return Metric('node_vmstat_%s' % (title,), value, { }, ts, instance)
