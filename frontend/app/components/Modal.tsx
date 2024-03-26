// components/Modal.js
const Modal = ({ children, onClose }) => {
  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex justify-center items-center mx-auto">
      <div className="bg-slate-300 p-4 rounded-lg shadow-lg">
        {children}
        <button onClick={onClose} className="text-cyan-500">
          Close
        </button>
      </div>
    </div>
  );
};

export default Modal;
