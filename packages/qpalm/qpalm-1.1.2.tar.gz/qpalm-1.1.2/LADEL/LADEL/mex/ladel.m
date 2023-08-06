classdef ladel < handle
    %Matlab interface for the LADEL C library
    %
    %ladel methods
    %
    %
    %
    %
    
    properties (SetAccess = private, Hidden = true)
        ncol;
    end
    
    methods
        
        %% Constructor - Create a new solver instance
        function obj = ladel(ncol)
            obj.ladel_mex('init', ncol);
        end

        %% Mex function
        varargout = ladel_mex(obj, varargin)
        
        function delete(obj)
            obj.ladel_mex('delete');
        end
        
        function varargout = factorize(obj, M, varargin)
            M = triu(M);
            if nargin == 3
                ordering = varargin{1};
                obj.ladel_mex('factorize', M, ordering);
            else
                obj.ladel_mex('factorize', M);
            end
            
            if nargout > 0
                if nargout == 2
                    [L, D] = obj.ladel_mex('return');
                    varargout{1} = L;
                    varargout{2} = D;
                elseif nargout == 3
                    [L, D, p] = obj.ladel_mex('return');
                    varargout{1} = L;
                    varargout{2} = D;
                    varargout{3} = p;
                else
                    error('Wrong number of output arguments for factorize');
                end
            end
        end
        
        function y = dense_solve(obj, x)
            y = obj.ladel_mex('solve', x);
        end
        
        function varargout = factorize_advanced(obj, M, Mbasis, varargin)
            M = triu(M);
            Mbasis = triu(Mbasis);
            if nargin == 4
                ordering = varargin{1};
                obj.ladel_mex('factorize_advanced', M, Mbasis, ordering);
            else
                obj.ladel_mex('factorize_advanced', M, Mbasis);
            end
            
            if nargout > 0
                if nargout == 2
                    [L, D] = obj.ladel_mex('return');
                    varargout{1} = L;
                    varargout{2} = D;
                elseif nargout == 3
                    [L, D, p] = obj.ladel_mex('return');
                    varargout{1} = L;
                    varargout{2} = D;
                    varargout{3} = p;
                else
                    error('Wrong number of output arguments for factorize_advanced');
                end
            end
                    
        end
        
        function varargout = factorize_with_prior_basis(obj, M)
            M = triu(M);         
            obj.ladel_mex('factorize_with_prior_basis', M);
            if nargout > 0
                if nargout == 2
                    [L, D] = obj.ladel_mex('return');
                    varargout{1} = L;
                    varargout{2} = D;
                elseif nargout == 3
                    [L, D, p] = obj.ladel_mex('return');
                    varargout{1} = L;
                    varargout{2} = D;
                    varargout{3} = p;
                else
                    error('Wrong number of output arguments for factorize_with_prior_basis');
                end
            end 
        end
        
        function varargout = row_mod(obj, row, varargin)
            
            if nargin ~= 2 && nargin ~= 4
                error('Wrong number of input arguments for row_mod.\n Use .row_mod(row) to delete a row (with index row) or .row_mod(row, w, diag_elem) to add a row w and with on the diagonal diag_elem.\n');
            end
            if nargin == 2
                obj.ladel_mex('rowmod', int64(row), length(row));
            else
                w = varargin{1};
                diag_elem = varargin{2};
                obj.ladel_mex('rowmod', int64(row), length(row), w, diag_elem);
            end
            
            if nargout > 0
                if nargout == 2
                    [L, D] = obj.ladel_mex('return');
                    varargout{1} = L;
                    varargout{2} = D;
                elseif nargout == 3
                    [L, D, p] = obj.ladel_mex('return');
                    varargout{1} = L;
                    varargout{2} = D;
                    varargout{3} = p;
                else
                    error('Wrong number of output arguments for factorized_advanced');
                end
            end
        end
    end
    
end

