import { useState, useEffect, useRef } from 'react';
import { Table, Input, Button, Space, Tag, Modal, Breadcrumb } from 'antd';
import { SearchOutlined, ReloadOutlined, HomeOutlined } from '@ant-design/icons';
import { createStyles } from 'antd-style';
import 'antd/dist/reset.css';

const { Search } = Input;

const useStyle = createStyles(({ css, token }) => {
  const { antCls } = token;
  return {
    customTable: css`
      ${antCls}-table {
        ${antCls}-table-container {
          ${antCls}-table-body,
          ${antCls}-table-content {
            scrollbar-width: thin;
            scrollbar-color: #eaeaea transparent;
            scrollbar-gutter: stable;
          }
        }
      }
    `,
  };
});

function AssetList() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [inputValue, setInputValue] = useState('');
  const [statusFilter, setStatusFilter] = useState(null);
  const { styles } = useStyle();
  const debounceTimer = useRef(null);
  
  // Modal state for children view
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [childrenData, setChildrenData] = useState([]);
  const [childrenLoading, setChildrenLoading] = useState(false);
  const [breadcrumbPath, setBreadcrumbPath] = useState([]);

  useEffect(() => {
    fetchAssets();
  }, [currentPage, searchTerm, statusFilter]);

  const fetchAssets = async () => {
    setLoading(true);
    try {
      let url = `/assets/?page=${currentPage}`;
      if (searchTerm) {
        url += `&search=${encodeURIComponent(searchTerm)}`;
      }
      if (statusFilter !== null) {
        url += `&is_active=${statusFilter}`;
      }
      
      console.log('Fetching URL:', url, 'Status Filter:', statusFilter);
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setAssets(data.results || []);
      setTotalCount(data.count || 0);
    } catch (error) {
      console.error('Error fetching assets:', error);
      setAssets([]);
      setTotalCount(0);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (value) => {
    setSearchTerm(value);
    setCurrentPage(1);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);

    // Clear existing timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    // Set new timer for debounced search
    debounceTimer.current = setTimeout(() => {
      setSearchTerm(value);
      setCurrentPage(1);
    }, 500);
  };

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, []);

  const handleTableChange = (pagination, filters) => {
    // Check if filter changed
    const newStatusFilter = filters.is_active && filters.is_active.length === 1 
      ? filters.is_active[0] 
      : null;
    
    const filterChanged = newStatusFilter !== statusFilter;
    
    // If filter changed, reset to page 1, otherwise use the clicked page
    if (filterChanged) {
      setCurrentPage(1);
      setStatusFilter(newStatusFilter);
    } else {
      setCurrentPage(pagination.current);
    }
  };

  const columns = [
    {
      title: 'Asset Name',
      dataIndex: 'asset_name',
      key: 'asset_name',
      width: 200,
      fixed: 'left',
      sorter: (a, b) => a.asset_name.localeCompare(b.asset_name),
    },
    {
      title: 'Asset Code',
      dataIndex: 'asset_code',
      key: 'asset_code',
      width: 150,
      fixed: 'left',
      render: (code) => <Tag color="blue">{code}</Tag>,
    },
    {
      title: 'Type',
      dataIndex: 'asset_type',
      key: 'asset_type',
      width: 150,
      sorter: (a, b) => a.asset_type.localeCompare(b.asset_type),
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
      width: 150,
      sorter: (a, b) => a.location.localeCompare(b.location),
    },
    {
      title: 'Manager',
      dataIndex: 'manager',
      key: 'manager',
      width: 150,
      sorter: (a, b) => a.manager.localeCompare(b.manager),
    },
    {
      title: 'Status',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (isActive) => (
        <Tag color={isActive ? 'green' : 'red'}>
          {isActive ? 'Active' : 'Inactive'}
        </Tag>
      ),
      filters: [
        { text: 'Active', value: true },
        { text: 'Inactive', value: false },
      ],
      filteredValue: statusFilter !== null ? [statusFilter] : null,
    },
    {
      title: 'Start Date',
      dataIndex: 'start_date',
      key: 'start_date',
      width: 120,
      sorter: (a, b) => new Date(a.start_date) - new Date(b.start_date),
    },
    {
      title: 'End Date',
      dataIndex: 'end_date',
      key: 'end_date',
      width: 120,
      sorter: (a, b) => new Date(a.end_date) - new Date(b.end_date),
    },
    {
      title: 'Action',
      key: 'action',
      fixed: 'right',
      width: 100,
      render: (_, record) => (
        <Space size="small">
          <a onClick={() => handleView(record)}>View</a>
          <a onClick={() => handleDelete(record)} style={{ color: 'red' }}>Delete</a>
        </Space>
      ),
    },
  ];

  const handleView = async (record) => {
    setChildrenLoading(true);
    setIsModalVisible(true);
    
    try {
      const response = await fetch(`/assets/${record.id}/children/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setChildrenData(data.children || []);
      setBreadcrumbPath([{ id: record.id, name: record.asset_name }]);
    } catch (error) {
      console.error('Error fetching children:', error);
      setChildrenData([]);
    } finally {
      setChildrenLoading(false);
    }
  };

  const handleViewChild = async (record) => {
    setChildrenLoading(true);
    
    try {
      const response = await fetch(`/assets/${record.id}/children/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setChildrenData(data.children || []);
      setBreadcrumbPath([...breadcrumbPath, { id: record.id, name: record.asset_name }]);
    } catch (error) {
      console.error('Error fetching children:', error);
      setChildrenData([]);
    } finally {
      setChildrenLoading(false);
    }
  };

  const handleBreadcrumbClick = async (index) => {
    if (index === breadcrumbPath.length - 1) return; // Already at this level
    
    setChildrenLoading(true);
    const targetAsset = breadcrumbPath[index];
    
    try {
      const response = await fetch(`/assets/${targetAsset.id}/children/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setChildrenData(data.children || []);
      setBreadcrumbPath(breadcrumbPath.slice(0, index + 1));
    } catch (error) {
      console.error('Error fetching children:', error);
      setChildrenData([]);
    } finally {
      setChildrenLoading(false);
    }
  };

  const handleModalClose = () => {
    setIsModalVisible(false);
    setChildrenData([]);
    setBreadcrumbPath([]);
  };

  const handleDelete = (record) => {
    if (confirm(`Are you sure you want to delete ${record.asset_name}?`)) {
      fetch(`/assets/${record.id}/`, {
        method: 'DELETE'
      })
      .then(() => {
        fetchAssets();
        alert('Asset deleted successfully!');
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error deleting asset');
      });
    }
  };

  const childrenColumns = [
    {
      title: 'Asset Name',
      dataIndex: 'asset_name',
      key: 'asset_name',
      width: 200,
    },
    {
      title: 'Asset Code',
      dataIndex: 'asset_code',
      key: 'asset_code',
      width: 150,
      render: (code) => <Tag color="blue">{code}</Tag>,
    },
    {
      title: 'Type',
      dataIndex: 'asset_type',
      key: 'asset_type',
      width: 150,
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
      width: 150,
    },
    {
      title: 'Manager',
      dataIndex: 'manager',
      key: 'manager',
      width: 150,
    },
    {
      title: 'Status',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (isActive) => (
        <Tag color={isActive ? 'green' : 'red'}>
          {isActive ? 'Active' : 'Inactive'}
        </Tag>
      ),
    },
    {
      title: 'Start Date',
      dataIndex: 'start_date',
      key: 'start_date',
      width: 120,
      sorter: (a, b) => new Date(a.start_date) - new Date(b.start_date),
    },
    {
      title: 'End Date',
      dataIndex: 'end_date',
      key: 'end_date',
      width: 120,
      sorter: (a, b) => new Date(a.end_date) - new Date(b.end_date),
    },
    {
      title: 'Action',
      key: 'action',
      width: 100,
      render: (_, record) => (
        <Space size="small">
          <a onClick={() => handleViewChild(record)}>View</a>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px', minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '24px' }}>
          <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>
            Asset Management System
          </h1>
          <p style={{ color: '#666', fontSize: '16px' }}>
            Manage your assets with Nexgensis
          </p>
        </div>

        {/* Search Bar */}
        <div style={{ marginBottom: '16px' }}>
          <Space size="middle">
            <Search
              placeholder="Search assets..."
              allowClear
              enterButton={<SearchOutlined />}
              size="large"
              value={inputValue}
              onChange={handleInputChange}
              onSearch={handleSearch}
              style={{ width: 400 }}
            />
            <Button 
              icon={<ReloadOutlined />} 
              size="large"
              onClick={() => {
                setSearchTerm('');
                setInputValue('');
                setStatusFilter(null);
                setCurrentPage(1);
              }}
            >
              Refresh
            </Button>
          </Space>
        </div>

        {/* Table */}
        <Table
          className={styles.customTable}
          columns={columns}
          dataSource={assets}
          rowKey="id"
          loading={loading}
          scroll={{ x: 'max-content', y: 55 * 10 }}
          pagination={{
            current: currentPage,
            pageSize: 10,
            total: totalCount,
            showSizeChanger: false,
            showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} assets`,
          }}
          onChange={handleTableChange}
        />

        {/* Children Modal */}
        <Modal
          title="Asset Children"
          open={isModalVisible}
          onCancel={handleModalClose}
          width={1200}
          footer={[
            <Button key="close" onClick={handleModalClose}>
              Close
            </Button>
          ]}
        >
          {/* Breadcrumb Navigation */}
          <Breadcrumb style={{ marginBottom: '16px' }}>
            <Breadcrumb.Item>
              <HomeOutlined />
            </Breadcrumb.Item>
            {breadcrumbPath.map((item, index) => (
              <Breadcrumb.Item key={item.id}>
                <a 
                  onClick={() => handleBreadcrumbClick(index)}
                  style={{ 
                    cursor: index === breadcrumbPath.length - 1 ? 'default' : 'pointer',
                    color: index === breadcrumbPath.length - 1 ? '#000' : '#1890ff'
                  }}
                >
                  {item.name}
                </a>
              </Breadcrumb.Item>
            ))}
          </Breadcrumb>

          {/* Children Table */}
          {childrenData.length === 0 && !childrenLoading ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
              No children found for this asset
            </div>
          ) : (
            <Table
              columns={childrenColumns}
              dataSource={childrenData}
              rowKey="id"
              loading={childrenLoading}
              pagination={false}
              scroll={{ x: 'max-content', y: 400 }}
            />
          )}
        </Modal>
      </div>
    </div>
  );
}

export default AssetList;
