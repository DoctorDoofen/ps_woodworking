import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, useParams } from 'react-router-dom';
import { createProduct, updateProduct, fetchProductDetails } from '../../redux/products';
import './ProductForm.css';
import { useModal } from '../../context/Modal';

function ProductForm() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { productId } = useParams();
  const productDetails = useSelector(state => state.products.productDetails);
  const [isEditMode, setIsEditMode] = useState(false);
  const [product_name, setProductName] = useState('');
  const [product_price, setProductPrice] = useState('');
  const [department, setDepartment] = useState('');
  const [quantity, setQuantity] = useState('');
  const [description, setDescription] = useState('');
  const [previewImage, setPreviewImage] = useState('');
  const [image1, setImage1] = useState('');
  const [image2, setImage2] = useState('');
  const [image3, setImage3] = useState('');
  const [image4, setImage4] = useState('');
  const { closeModal } = useModal()


  useEffect(() => {
    if (productId) {
      setIsEditMode(true);
      dispatch(fetchProductDetails(productId));
    }
  }, [dispatch, productId]);

  useEffect(() => {
    if (isEditMode && productDetails) {
      setProductName(productDetails.name || '');
      setProductPrice(productDetails.price || '');
      setDepartment(productDetails.department || '');
      setQuantity(productDetails.quantity || '');
      setDescription(productDetails.description || '');
      setPreviewImage(productDetails.productImages[0].url || '');
      setImage1(productDetails.productImages.length >= 1 && (productDetails.productImages[0].url || ''));
      setImage2(productDetails.productImages.length >= 2 && (productDetails.productImages[1].url || ''));
      setImage3(productDetails.productImages.length >= 3 && (productDetails.productImages[2].url || ''));
      setImage4(productDetails.productImages.length == 4 && (productDetails.productImages[3].url || ''));
    } else if (!isEditMode) {
      setProductName('');
      setProductPrice('');
      setDepartment('');
      setQuantity('');
      setDescription('');
      setPreviewImage('');
      setImage1('');
      setImage2('');
      setImage3('');
      setImage4('');
    }
  }, [isEditMode, productDetails]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const product = {
      product_name,
      product_price,
      description,
      department,
      quantity,
      previewImage,
      image1,
      image2,
      image3,
      image4
    }

    try {
      if (isEditMode && productId) {
        dispatch(updateProduct(productId, product)).then((res) => {
          navigate(`/products/${res.id}`);
          closeModal()
        });
      } else {
        dispatch(createProduct(product)).then((res) => {
          navigate(`/products/${res.id}`);
          closeModal()
        });
      }
    } catch (err) {
      console.error('Error creating/updating product:', err);
      // Handle error
    }
  };

  const onCancelHandler = () => {
    if (isEditMode && productId)
      navigate('/products/current')
    else
      closeModal()
  }

  if (isEditMode && productId && !productDetails) return null;

  return (
    <div className="modal-content">
      <h1 className='model-header'>{isEditMode ? 'Edit Product' : 'Add New Product'}</h1>
      <form onSubmit={handleSubmit}>
        {/* Product Details Fields */}
        <div className="form-group">
          <label htmlFor="product_name">Name:</label>
          <input type="text" id="product_name" value={product_name} onChange={(e) => setProductName(e.target.value)} required />
        </div>
        <div className="form-group">
          <label htmlFor="product_price">Price:</label>
          <input type="number" id="product_price" value={product_price} onChange={(e) => setProductPrice(parseFloat(e.target.value))} required />
        </div>
        <div className="form-group">
          <label htmlFor="department">Department:</label>
          <input type="text" id="department" value={department} onChange={(e) => setDepartment(e.target.value)} />
        </div>
        <div className="form-group">
          <label htmlFor="quantity">Quantity:</label>
          <input type="number" id="quantity" value={quantity} onChange={(e) => setQuantity(parseInt(e.target.value))} required />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description:</label>
          <textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} required />
        </div>

        {/* Image Handling */}
        <h2>Product Images</h2>
        <div className="form-group">
          <label htmlFor="previewImage">Preview Image:</label>
          <input type="url" id="previewImage" value={previewImage} onChange={(e) => setPreviewImage(e.target.value)} required />
          {previewImage && <img src={previewImage} alt="Preview" style={{ maxWidth: '100px', maxHeight: '100px' }} />}
        </div>
        <div className="form-group">
          <label htmlFor="image1">Image 1 (Optional):</label>
          <input type="url" id="image1" value={image1} onChange={(e) => setImage1(e.target.value)} />
          {image1 && <img src={image1} alt="Image 1" style={{ maxWidth: '100px', maxHeight: '100px' }} />}
        </div>
        <div className="form-group">
          <label htmlFor="image2">Image 2 (Optional):</label>
          <input type="url" id="image2" value={image2} onChange={(e) => setImage2(e.target.value)} />
          {image2 && <img src={image2} alt="Image 2" style={{ maxWidth: '100px', maxHeight: '100px' }} />}
        </div>
        <div className="form-group">
          <label htmlFor="image3">Image 3 (Optional):</label>
          <input type="url" id="image3" value={image3} onChange={(e) => setImage3(e.target.value)} />
          {image3 && <img src={image3} alt="Image 3" style={{ maxWidth: '100px', maxHeight: '100px' }} />}
        </div>
        <div className="form-group">
          <label htmlFor="image4">Image 4 (Optional):</label>
          <input type="url" id="image4" value={image4} onChange={(e) => setImage4(e.target.value)} />
          {image4 && <img src={image4} alt="Image 4" style={{ maxWidth: '100px', maxHeight: '100px' }} />}
        </div>

        <div className="form-actions">
          <button type="submit">{isEditMode ? 'Update Product' : 'Add Product'}</button>
          <button type="button" onClick={onCancelHandler}>Cancel</button>
        </div>
      </form>
    </div>
  );
}

export default ProductForm;
